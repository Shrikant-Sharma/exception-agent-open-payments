"""Run tracing with MLflow. Optional: step 5 turns it on with --trace.

Two words to know.
  A trace is one request from start to finish. Here: one exception.
  A span is one step inside a trace, with its own inputs, outputs, start and end.
  Here: each model call is a span, each lookup is a span, and the exception as a
  whole is the root span that holds them.

Nothing in the agent loop changes. The model and the lookups are wrapped from the
outside: each wrapper opens a span, calls the real thing, and records what went in,
what came out, the tokens and the time. A run without --trace never imports MLflow.

Traces are stored in a local file, mlflow.db, in the project folder. To look at them:

    mlflow ui --backend-store-uri sqlite:///mlflow.db        then open http://127.0.0.1:5000

Set MLFLOW_TRACKING_URI to send them to an MLflow server instead.
"""
import contextlib
import os

from common import ROOT

EXPERIMENT = "exception-agent"


class Tracer:
    def __init__(self, tag, tools_via="direct"):
        import mlflow
        from mlflow.entities import SpanType
        from mlflow.tracing.constant import SpanAttributeKey
        self.mlflow, self.types, self.keys = mlflow, SpanType, SpanAttributeKey
        self.tag, self.tools_via = tag, tools_via
        if not os.environ.get("MLFLOW_TRACKING_URI"):
            mlflow.set_tracking_uri("sqlite:///" + (ROOT / "mlflow.db").as_posix())
        self.experiment_id = mlflow.set_experiment(experiment_name=EXPERIMENT).experiment_id
        self.trace_ids = {}

    def model(self, inner):
        return TracedModel(inner, self)

    def lookups(self, inner):
        return TracedLookups(inner, self)

    @contextlib.contextmanager
    def exception(self, case):
        """The root span: one exception, from the case the agent is handed to the checked result."""
        with self.mlflow.start_span(name=case["exception_id"], span_type=self.types.AGENT) as span:
            span.set_inputs({"case": case["text"]})
            self.mlflow.update_current_trace(tags={"run": self.tag, "exception_id": case["exception_id"], "check": case["check"]},
                                             request_preview=case["text"].splitlines()[0])
            holder = {}
            yield holder
            rec = holder.get("rec")
            if rec:
                span.set_outputs({k: rec[k] for k in ("status", "reason", "root_cause", "action", "fix_value", "explanation")})
                span.set_attributes({
                    "checks": [step["check"] for step in rec["trace"] if "check" in step],
                    "conclusions": rec["n_conclusions"], "lookups": rec["lookups"], "model_calls": rec["model_calls"],
                    "tokens_in": rec["tokens_in"], "tokens_out": rec["tokens_out"], "model_seconds": rec["seconds"],
                })
                self.mlflow.update_current_trace(response_preview=" ".join(filter(None, [rec["status"] + ":", rec["root_cause"], rec["fix_value"]])))
            self.trace_ids[case["exception_id"]] = span.trace_id

    def flush(self):
        self.mlflow.flush_trace_async_logging()


class TracedModel:
    """The model, with a span around every call. Everything else is passed through to the real model."""

    def __init__(self, inner, tracer):
        self.inner, self.tracer = inner, tracer

    def __getattr__(self, name):
        return getattr(self.inner, name)

    def ask(self, messages, schema, max_tokens):
        t = self.tracer
        with t.mlflow.start_span(name="model call", span_type=t.types.CHAT_MODEL) as span:
            span.set_inputs({"messages": messages, "max_tokens": max_tokens})
            span.set_attribute(t.keys.MODEL, self.inner.name)
            obj, usage = self.inner.ask(messages, schema, max_tokens)
            span.set_outputs(obj)
            span.set_attribute(t.keys.CHAT_USAGE, {"input_tokens": usage["tokens_in"], "output_tokens": usage["tokens_out"],
                                                   "total_tokens": usage["tokens_in"] + usage["tokens_out"]})
            span.set_attribute("model_seconds", usage["seconds"])
            return obj, usage


class TracedLookups:
    """The lookups, with a span around every call."""

    def __init__(self, inner, tracer):
        self.inner, self.tracer = inner, tracer

    def __getattr__(self, name):
        return getattr(self.inner, name)

    def run(self, name, text, case):
        t = self.tracer
        with t.mlflow.start_span(name=name, span_type=t.types.TOOL) as span:
            span.set_inputs({"input": text})
            span.set_attribute("via", t.tools_via)
            said, facts = self.inner.run(name, text, case)
            span.set_outputs({"text": said, "facts": facts})
            return said, facts

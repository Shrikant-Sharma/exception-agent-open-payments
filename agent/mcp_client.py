"""The agent's side of MCP: the same four lookups, called through the MCP server instead of directly.

McpLookups has the same one method as agent.tools.Lookups, run(name, text, case),
and returns the same two things: the text the model reads and the facts as data.
So the loop does not know or care which one it was given.

How it works. The MCP client library is asynchronous and the agent loop is not.
A small background thread keeps one connection to the server open for the whole
run, and each lookup is handed to that thread and waited for.
"""
import asyncio
import concurrent.futures
import sys
import threading
import time

from mcp import Client, StdioServerParameters

from common import ROOT

SERVER = ROOT / "mcp_server.py"
# How each lookup's one text input maps onto the arguments of its MCP tool.
ARGUMENTS = {
    "registry_lookup": lambda text, case: {"npi": text},
    "registry_search": lambda text, case: {"name": text, "line_npi": case["npi"]},
    "ledger_history": lambda text, case: {"name": text},
    "source_documents": lambda text, case: {"line_ids": text},
}


class McpLookups:
    def __init__(self, registry_down=False, timeout=60):
        self.timeout = timeout
        self.calls, self.seconds = 0, 0.0
        args = [str(SERVER)] + (["--registry-down"] if registry_down else [])
        self.params = StdioServerParameters(command=sys.executable, args=args, cwd=str(ROOT))
        self.loop = asyncio.new_event_loop()
        self.queue = None
        ready = concurrent.futures.Future()
        self.thread = threading.Thread(target=self._thread, args=(ready,), daemon=True)
        self.thread.start()
        self.tools = ready.result(timeout)          # raises here if the server did not start

    # ---- the background thread: one connection, kept open, serving requests in order
    def _thread(self, ready):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._serve(ready))

    async def _serve(self, ready):
        self.queue = asyncio.Queue()
        try:
            async with Client(self.params) as client:
                listed = await client.list_tools()
                ready.set_result([{"name": t.name, "description": (t.description or "").strip(),
                                   "arguments": sorted((t.input_schema or {}).get("properties", {}))} for t in listed.tools])
                while True:
                    item = await self.queue.get()
                    if item is None:
                        return
                    name, arguments, done = item
                    try:
                        done.set_result(await client.call_tool(name, arguments))
                    except Exception as e:          # hand the error to the caller's thread
                        done.set_exception(e)
        except Exception as e:
            if not ready.done():
                ready.set_exception(e)

    # ---- what the agent loop calls
    def run(self, name, text, case):
        """Returns (text for the model, facts as a dict), exactly as agent.tools.Lookups.run does."""
        arguments = ARGUMENTS[name]((text or "").strip(), case)
        done = concurrent.futures.Future()
        t0 = time.time()
        self.loop.call_soon_threadsafe(self.queue.put_nowait, (name, arguments, done))
        result = done.result(self.timeout)
        self.calls += 1
        self.seconds += time.time() - t0
        if result.is_error:
            raise RuntimeError(f"MCP tool {name} failed: {result.content[0].text if result.content else 'no message'}")
        return result.content[0].text, (result.structured_content or {}).get("facts", {})

    def close(self):
        if self.thread.is_alive():
            self.loop.call_soon_threadsafe(self.queue.put_nowait, None)
            self.thread.join(10)

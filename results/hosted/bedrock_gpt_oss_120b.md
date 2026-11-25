# Step 12. The agent on a hosted model: bedrock_gpt_oss_120b

Model `openai.gpt-oss-120b-1:0`, run as endpoint https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1. Lookups: direct. Same procedure, lookups and code checks as the laptop runs. Temperature 0.

**The regression check: PASSED.** The bar is right >= 33 and wrong <= 0 on the 35 development exceptions. This model: 35 right, 0 to a person, 0 wrong.

Stopped after the regression check, as asked. The test has not been run for this model.

| Stage | Exceptions | Right | To a person | Wrong | Laptop model: right, to a person, wrong | Tokens in | Tokens out | Median seconds per exception | Cost |
|---|---|---|---|---|---|---|---|---|---|
| Development (the regression check) | 35 | 35 | 0 | 0 | 35, 0, 0 | 108,719 | 27,770 | 6.1 | $0.03 |

In all: 123 model calls, 108,719 tokens in and 27,770 out, $0.03 at $0.15 per million tokens in and $0.6 out.

## How to read this

- The laptop model was scored on the same 95 exceptions first. A hosted model's score is a second use of that test: it is a fair comparison of the two models, and it is no longer an unseen test for the project as a whole.
- A proposal is counted wrong only when it passed the checks and does not match the answer key. "To a person" means the agent or the checks handed the exception over, which is the safe outcome.
- In the registry-down test the right outcome for an identity exception is to hand it to a person.
- Seconds are the time the service took to answer, summed over an exception's model calls. They include the service's queue and any waiting on a rate limit inside one request.

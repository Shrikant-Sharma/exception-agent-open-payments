# Decisions

This is my log of the choices I made while running this project on my own machine.
Each entry has the situation, the options, my choice, my reason, and what happened.

## 1. Which test result I quote (November 25, 2026)

**Situation.** I ran the 95 test exceptions on my own laptop. The model was Qwen3 4B,
on 8 threads of a Ryzen 7 4800H, with llama-cpp-python 0.3.36. My run ended with 86
right, 9 sent to a person and 0 wrong. The reference run was made on another machine,
on 2 CPU cores, with llama-cpp-python 0.3.37. It ended with 88, 7 and 0. The model
file, the procedure and the data were the same, and both ran at temperature 0.

**Options.**

- A. Quote my own run: 86, 9 and 0.
- B. Quote the reference run: 88, 7 and 0.
- C. Run the test again on 2 threads, or build version 0.3.37, to try to reach 88.

**Choice.** A.

**Reason.** A number is mine only after my own run. Option B quotes a run I did not
make. Option C runs the test again to chase a number. Picking the best of several
test runs is a quiet way of tuning on the test, and I do not tune on the test.

**What happened.** 89 of the 95 exceptions ended the same way in both runs. Six ended
differently. Four went to a person in my run and were right in the reference: E-018,
E-082, E-097 and E-112. Two were right in my run and went to a person in the
reference: E-092 and E-109. No wrong proposal passed the checks in either run. In my
run the checks stopped 8 wrong proposals, counting every try. Three things differ
between the two runs: the library version, the thread count and the machine. I cannot
say which of them moved the six, so I do not claim to know.

**How I say it.** On my laptop, 86 of 95 ended right, 9 went to a person and none
were wrong. The reference run on another machine gave 88, 7 and 0. Six exceptions
ended differently, four one way and two the other, and no wrong proposal passed on
either.

## 2. What to do when Bedrock's replies could not be read (November 25, 2026)

**Situation.** My first call to a hosted model, gpt-oss-120b on Amazon Bedrock, sent
the exception to a person after one lookup. I read the run's record. The model had
not judged the case. Its replies could not be read as JSON. I printed the raw
replies. In four of five, Bedrock had put a stray `{"` in front of a correct JSON
object, like this: `{"{"lookup":"registry_lookup", ...}`. The model's reasoning
followed the procedure correctly. Only the wrapping of the answer was broken. The
code read from the first opening brace to the last closing brace, so it could not
parse the reply. This path had only been run against stand-in services before, and
a stand-in sends tidy replies.

**Options.**

- A. A small fix in how a hosted reply is read: when the reply does not parse, try
  the next opening brace.
- B. Switch to Groq's free tier and change no code.
- C. Stop and send the problem back to the chat that built the project.

**Choice.** A.

**Reason.** It keeps the run on Bedrock. It touches only the hosted path in
`agent/llm.py`, so the laptop model's code and every stored result stay as they
were. A wrong read cannot slip through, because whatever is read is still checked
against the schema and then against every code check. Option B would leave Bedrock
unrun. Option C would cost a day while a short-lived key ran out.

**What happened.** The fix is a helper of about ten lines, `json_object_in`, and one
changed line in `EndpointModel.ask`. The endpoint tests still pass, 23 of 23. No
check was loosened.

**How I say it.** My first real call to Bedrock found something the stand-in tests
could not. The exception went to a person, which is the safe outcome, but for the
wrong reason. I printed the raw reply, saw a stray opening in front of the JSON,
and fixed the reader without loosening a single check.

## 3. Which hosted model sees the test (November 25, 2026)

**Situation.** Only one hosted model may see the 95 test exceptions. The test is not
for shopping between models. Before any of them saw it, I ran the regression check
on three candidates on Amazon Bedrock, US East (N. Virginia), on the 35 development
exceptions. I had said in advance that I would judge on the regression result, cost
and time.

| Candidate | Right, to a person, wrong | First conclusion passed | Tokens in | Tokens out | Median seconds | Cost for the 35 |
|---|---|---|---|---|---|---|
| gpt-oss-120b, default reasoning effort | 35, 0, 0 | 35 of 35 | 108,719 | 27,770 | 6.1 | $0.033 |
| gpt-oss-20b | 35, 0, 0 | 33 of 35 | 127,964 | 30,978 | 9.2 | $0.018 |
| gpt-oss-120b, low reasoning effort | 35, 0, 0 | 35 of 35 | 104,587 | 10,753 | 4.1 | $0.022 |

Prices are AWS's list prices as I read them that day: $0.15 in and $0.60 out per
million tokens for gpt-oss-120b, and $0.07 and $0.30 for gpt-oss-20b.

**Options.**

- A. gpt-oss-120b at default effort. The most reasoning, so the most room on harder
  cases. The dearest and not the fastest.
- B. gpt-oss-20b. The lowest price per token. The slowest, with the most tokens, and
  the only one whose first conclusion was sent back, twice.
- C. gpt-oss-120b at low effort. The same model as A with 61 percent less output,
  the fastest, and no conclusion sent back.

**Choice.** C.

**Reason.** The regression check could not separate them. All three passed at 35 of
35. So I went to the other two things I had named. On time, C was first. On cost, it
was within half a cent of the cheapest, and the whole gap between the three is a few
cents, so cost did not decide it. C also had no conclusion sent back. The risk I
accept is that less reasoning may cost something on harder unseen cases. The 35
cannot tell me that. The test will.

**A side finding.** Both of the 20b's sent-back conclusions were correct answers.
The check that an explanation is in English refused them over a curly apostrophe.
The check is a little too strict. I left it alone, because too strict is the safe
direction.

**What happened.** On the 95 test exceptions the model ended 93 right, 2 sent to a
person and 0 wrong. My laptop model, Qwen3 4B, ended 86, 9 and 0 on the same 95.
This is a second use of that test, so it is a fair comparison of two models and no
longer an unseen test for the project.

| On the 95 test exceptions | gpt-oss-120b, low effort, on Bedrock | Qwen3 4B on my laptop |
|---|---|---|
| Right, to a person, wrong | 93, 2, 0 | 86, 9, 0 |
| First conclusion right and passed | 91 | 72 |
| First conclusions the checks sent back | 2 | 20 |
| Wrong proposals stopped, counting every try | 3 | 8 |
| Wrong proposals that passed | 0 | 0 |
| Median seconds per exception | 4.0 | 24.6 |
| Tokens in and out | 295,711 and 31,269 | 390,634 and 14,318 |
| Cost at list price | $0.06 | No API cost |

Nine exceptions ended differently. Eight were right on the hosted model and went to
a person on my laptop: E-018, E-032, E-033, E-082, E-090, E-095, E-097 and E-112.
One went the other way: E-089. Both of the hosted model's hand-offs, E-089 and
E-108, named the right NPI in the same answer and still said it could not confirm.
That is the weak point I already knew about: a hand-off whose stated facts are true
passes the checks.

Both stress tests ended 21 of 21 as the answer key says. With the registry down the
model handed all 21 to a person. With an instruction planted in the record, no
exception was closed the way the note asked.

The whole run, with the regression check and both stress tests, cost $0.12 at list
price: 635 model calls, 565,455 tokens in and 55,711 out. The risk I accepted did
not show: low effort was enough on these cases.

**How I say it.** Three hosted candidates all passed my regression check at 35 of
35, so the check could not choose between them. I chose on time and cost, wrote the
choice down, and only then ran the test. That model ended 93 of 95 right with none
wrong, against 86 on my laptop model, for 12 cents.

## 4. My own change: a hand-off that names a fix is sent back (November 25, 2026)

**Situation.** The checks pass a hand-off when the facts it states are true. So the
agent can find the right NPI, write it in its answer, and still say it cannot
confirm. I saw this on both of my models. On the development exceptions it shows
with the weakest model only: in the stored run of Qwen2.5 1.5B, exceptions E-096 and
E-106 were handed to a person while the answer itself named a valid corrected NPI.

**Options.**

- A. A stricter rule in `agent/checks.py`: a hand-off that names a corrected NPI is
  sent back, when that NPI came back from the registry in this case, is active and
  carries the name on the line.
- B. A check on city and practitioner type, so the same-name twins raise an
  exception.
- C. No code change: rerun the development exceptions on 2 threads to see whether
  the thread count alone changes the answers.

**Choice.** A.

**Reason.** It goes after the one weakness that showed on both a 4-billion and a
120-billion parameter model. It is the smallest change of the three, in a file I
have read line by line. And it makes a prediction that can fail.

**How I built it.** The rule is off unless I set `AGENT_STRICT_HANDOFF=1`. Every
stored result was made with it off, so those results and the tests still reproduce.
The run's record now says whether the rule was on. The message sent back repeats
what the agent wrote. It never gives the answer.

**How I try it.** On the 35 development exceptions only, with Qwen2.5 1.5B on my
laptop: one run with the rule off, one with it on. I do not judge it on the test.
The idea came partly from what the test showed, so the test cannot be its judge.

**My prediction, written before the run.** The rule fires on a few hand-offs. The
count of right answers goes up by one at most, not by two. In the stored run, E-096
hands off on its third and last try, so being sent back cannot help it. E-106 hands
off on its second try, so it has one try left. Wrong stays at 0, because a proposal
still has to pass every other check. Model calls go up a little. On my 4B model and
on the hosted model the development result does not move: 35 of 35.

**What happened.** Two runs of the 35 development exceptions with Qwen2.5 1.5B on my
laptop, the same in everything but the rule.

| | Rule off | Rule on |
|---|---|---|
| Right, to a person, wrong | 18, 17, 0 | 19, 16, 0 |
| Regression check | FAIL | FAIL |
| Wrong proposals stopped, counting every try | 29 | 29 |
| Model calls | 223 | 224 |
| Exceptions identical step for step | | 33 of 35 |

The rule fired in two exceptions. In E-028 it turned a hand-off into the right fix.
The agent had written the right NPI, 1962429837, and still said it could not
confirm. With the rule on, the reason sent back said so, and on its last try the
agent proposed that NPI and passed every check. In E-106 the rule fired twice and
the agent repeated the same hand-off both times, so it still went to a person.

**My prediction against the result.** I was right on the count: one more right, not
two. I was right that wrong stays at 0 and that model calls go up a little. I was
wrong about which exception. I expected E-106 to recover, and it did not. The gain
came from E-028, which I had not named. E-096 never reached the rule on my machine.

**What I claim, and what I do not.** The rule recovered one hand-off out of two it
fired on, on a weak model, and let nothing wrong through. That is one exception, so
it shows the rule can work, not how often it does. The smaller model still fails
the regression check with or without it. On my 4B model and on the hosted model I
replayed every stored development conclusion through the rule and it never fires,
so those results stand at 35 of 35. I did not judge the rule on the test. A fair
test of it needs new exceptions from a new seed.

**How I say it.** Both my models sometimes found the right answer and handed off
anyway. I added a rule that sends such a hand-off back, behind a switch, and tried
it on the development exceptions with a weaker model. I predicted one more right
answer and no wrong ones. That is what I got, though from a different exception
than I expected.

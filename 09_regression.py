"""Step 9. The pass or fail check to run before any change to the model or the procedure ships.

It runs the agent on the development exceptions and compares the score with a
stored bar. It fails if fewer exceptions end right than the bar allows, or if
more wrong proposals pass the checks than before.

    python 09_regression.py --set-bar dev     store the bar from an existing run (here: the run tagged 'dev')
    python 09_regression.py                   run the agent now and compare with the bar
    python 09_regression.py --tag NAME        compare an existing run without running the agent again

Exit code 0 is a pass and 1 is a fail, so a build pipeline can block on it
(.github/workflows/regression.yml).
"""
import argparse
import importlib
import shutil
import subprocess
import sys

from common import RESULTS, ROOT, read_json, write_json

BAR = RESULTS / "regression_bar.json"
SLACK = 2          # exceptions the 'right' count may fall below the bar before the check fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set-bar")
    ap.add_argument("--tag")
    a = ap.parse_args()
    evaluate = importlib.import_module("06_evaluate").evaluate

    if a.set_bar:
        s = evaluate(a.set_bar, quiet=True)
        m = read_json(RESULTS / "runs" / a.set_bar / "run_manifest.json")
        write_json(BAR, {"from_run": a.set_bar, "model": m["model"], "procedure_sha256": m["procedure_sha256"],
                         "exceptions": s["exceptions"], "right": s["right"], "to_a_person": s["to_a_person"], "wrong": s["wrong"],
                         "passes_when": f"right >= {s['right'] - SLACK} and wrong <= {s['wrong']}"})
        print(f"Bar stored from run '{a.set_bar}': {s['right']} of {s['exceptions']} right, {s['wrong']} wrong ({m['model']}).")
        return

    bar = read_json(BAR)
    tag = a.tag
    if not tag:
        tag = "regression"
        shutil.rmtree(RESULTS / "runs" / tag, ignore_errors=True)
        subprocess.run([sys.executable, str(ROOT / "05_run_agent.py"), "--split", "dev", "--tag", tag], check=True)
    s = evaluate(tag, quiet=True)
    m = read_json(RESULTS / "runs" / tag / "run_manifest.json")
    if s["exceptions"] != bar["exceptions"]:
        print(f"FAIL: the run covers {s['exceptions']} exceptions, the bar was set on {bar['exceptions']}.")
        sys.exit(1)
    ok_right = s["right"] >= bar["right"] - SLACK
    ok_wrong = s["wrong"] <= bar["wrong"]
    print(f"Bar ({bar['model']}):   {bar['right']} of {bar['exceptions']} right, {bar['to_a_person']} to a person, {bar['wrong']} wrong")
    print(f"This run ({m['model']}): {s['right']} of {s['exceptions']} right, {s['to_a_person']} to a person, {s['wrong']} wrong")
    print(f"Right at least {bar['right'] - SLACK}: {'yes' if ok_right else 'NO'}.  Wrong no more than {bar['wrong']}: {'yes' if ok_wrong else 'NO'}.")
    passed = ok_right and ok_wrong
    write_json(RESULTS / "runs" / tag / "regression_result.json",
               {"passed": passed, "bar": bar, "this_run": {"model": m["model"], "right": s["right"], "to_a_person": s["to_a_person"], "wrong": s["wrong"]}})
    print("PASS" if passed else "FAIL")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()

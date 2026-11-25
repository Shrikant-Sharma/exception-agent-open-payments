"""Step 3. Build the scenario: a source ledger, a draft filing, and errors with known answers.

Public data only shows what a company filed. Nobody publishes their source
ledger, and nobody publishes their mistakes. So the test is built the way a
control is tested in practice: start from records known to be right, plant
errors with a fixed seed, and keep the answer key in a separate file.

What is real:      every payment fact (who, how much, when, what for) and
                   every registry record.
What is generated: the bookkeeping fields on each ledger line (document
                   number, feed, load date) and every planted error.

Outputs (data/scenario/):
  ledger_clean.csv   the ledger as the published records imply, no errors
  ledger.csv         the ledger with source errors planted
  draft_filing.csv   the filing built from that ledger, with transfer errors planted
  truth.csv          the answer key. No lookup the agent can call reads this file.
  splits.csv         which exceptions are development and which are test (keys only, no answers)

    python 03_build_scenario.py            rebuild from the seed and compare with the stored files
    python 03_build_scenario.py --rebuild  replace the stored files
"""
import collections
import datetime as dt
import json
import random
import shutil
import sys
import tempfile
from pathlib import Path

from common import (EXTRACT_CSV, FILING_CSV, LEDGER_CSV, SCENARIO_DIR, SEED, TRUTH_CSV,
                    first_names_agree, full_name, last_names_agree, load_rules,
                    name_agrees_with_registry, npi_check_digit_ok, read_csv, sha256_of, tokens, write_csv, write_json)
from registry import Registry

LEDGER_FIELDS = ["line_id", "record_id", "recipient_kind", "name", "first", "middle", "last", "npi",
                 "city", "state", "recipient_type", "amount", "pay_date", "nature", "product",
                 "document", "feed", "loaded_on", "note"]
FILING_FIELDS = ["filing_id", "line_id", "name", "first", "middle", "last", "npi", "city", "state",
                 "recipient_type", "amount", "pay_date", "nature", "product"]
TRUTH_FIELDS = ["case_id", "kind", "split", "check", "key", "lines", "expected_root_cause",
                "expected_action", "expected_value", "raised_by", "detail"]

# How many of each error to plant.
N_KEYED_WRONG = 22          # NPI typed wrong on one line
N_KEYED_TWIN = 4            # ...of which this many on a recipient who has a same-name twin in the registry
N_WRONG_SAME_LAST = 12      # line points at another person with the same last name
N_WRONG_SAME_FIRST = 6      # line points at another person with the same first name
N_WRONG_TWIN = 4            # as above, on a recipient who has a same-name twin
N_SILENT_TWIN = 4           # line points at the same-name twin: no rule can see this
N_UNCONFIRMABLE = 6         # NPI typed wrong on a recipient whose name the registry cannot support
N_LOADED_TWICE = 22         # one document loaded twice
N_SMALL_DROPPED = 12        # recipients whose small payments were all left out of the filing
N_AMOUNT_SWAPPED = 15       # two digits of the amount swapped in the filing
N_YEAR_WRONG = 10           # payment year typed as 2024 in the filing
DEV_SHARE = 0.27            # share of each kind set aside for developing the procedure
RELOAD_MONTHS = ("06", "09")  # the double loads are planted in two reload batches


def iso(mdy):
    m, d, y = mdy.split("/")
    return f"{y}-{m}-{d}"


def loaded_on(pay_date, reload=False):
    """Monthly load: lines are loaded on the 3rd of the following month; a reload runs on the 17th."""
    y, m, _ = (int(x) for x in pay_date.split("-"))
    y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return dt.date(y, m, 17 if reload else 3).isoformat()


def build_clean_ledger(rows):
    rows = sorted(rows, key=lambda r: (iso(r["date_of_payment"]), int(r["record_id"])))
    seq = collections.Counter()
    ledger = []
    for i, r in enumerate(rows, 1):
        person = bool(r["covered_recipient_npi"])
        nature = r["nature_of_payment_or_transfer_of_value"]
        feed = "expense reports" if nature in ("Food and Beverage", "Travel and Lodging", "Education") else "accounts payable"
        prefix = "EXP" if feed == "expense reports" else "AP"
        seq[prefix] += 1
        pay = iso(r["date_of_payment"])
        ledger.append({
            "line_id": f"L{i:05d}",
            "record_id": r["record_id"],
            "recipient_kind": "person" if person else "organization",
            "name": full_name(r["covered_recipient_first_name"], r["covered_recipient_middle_name"],
                              r["covered_recipient_last_name"], r["covered_recipient_name_suffix"]) if person else r["teaching_hospital_name"],
            "first": r["covered_recipient_first_name"], "middle": r["covered_recipient_middle_name"],
            "last": r["covered_recipient_last_name"],
            "npi": r["covered_recipient_npi"],
            "city": r["recipient_city"].upper(), "state": r["recipient_state"],
            "recipient_type": r["covered_recipient_primary_type_1"],
            "amount": f'{float(r["total_amount_of_payment_usdollars"]):.2f}',
            "pay_date": pay, "nature": nature,
            "product": r["name_of_drug_or_biological_or_device_or_medical_supply_1"],
            "document": f"{prefix}-25-{seq[prefix]:06d}", "feed": feed,
            "loaded_on": loaded_on(pay), "note": "",
        })
    return ledger


def mutate_npi(npi, rng, reg):
    """One wrong digit or two neighbouring digits swapped. Retry until the result has a bad
    check digit and is nobody's NPI, as a real typing error almost always does."""
    for _ in range(200):
        d = list(npi)
        if rng.random() < 0.5:
            i = rng.randrange(10)
            d[i] = rng.choice([c for c in "0123456789" if c != d[i]])
            how = "one digit wrong"
        else:
            i = rng.randrange(9)
            if d[i] == d[i + 1]:
                continue
            d[i], d[i + 1] = d[i + 1], d[i]
            how = "two digits swapped"
        new = "".join(d)
        if new != npi and not npi_check_digit_ok(new) and reg.lookup(new) is None:
            return new, how
    raise RuntimeError("could not mutate " + npi)


def swap_amount_digits(amount, rng):
    digits = [c for c in amount if c != "."]
    for _ in range(100):
        i = rng.randrange(len(digits) - 1)
        if digits[i] != digits[i + 1]:
            digits[i], digits[i + 1] = digits[i + 1], digits[i]
            s = "".join(digits)
            new = f"{int(s[:-2] or '0')}.{s[-2:]}"
            if float(new) != float(amount):
                return f"{float(new):.2f}"
            digits = [c for c in amount if c != "."]
    raise RuntimeError("could not swap " + amount)


FILES = ["ledger_clean.csv", "ledger.csv", "draft_filing.csv", "truth.csv", "splits.csv"]


def main():
    """Build into a scratch folder first. If a stored scenario exists, compare and leave it alone
    unless --rebuild is given, so the stored agent runs always match the stored scenario."""
    with tempfile.TemporaryDirectory() as tmp:
        build(Path(tmp))
        built = {f: sha256_of(Path(tmp) / f) for f in FILES}
        stored = {f: sha256_of(SCENARIO_DIR / f) for f in FILES if (SCENARIO_DIR / f).exists()}
        if len(stored) == len(FILES) and "--rebuild" not in sys.argv:
            same = built == stored
            print("\nThe scenario rebuilt from the seed matches the stored files." if same else
                  "\nTHE REBUILT SCENARIO DIFFERS FROM THE STORED FILES. A different Python version can change the random draws.\n"
                  "The stored files were left as they are, because the stored agent runs belong to them. Use --rebuild to replace them.")
            sys.exit(0 if same else 1)
        SCENARIO_DIR.mkdir(parents=True, exist_ok=True)
        for f in FILES:
            shutil.copy(Path(tmp) / f, SCENARIO_DIR / f)
        write_json(SCENARIO_DIR / "manifest.json", {"built_by": "03_build_scenario.py", "seed": SEED,
                                                    "extract_sha256": sha256_of(EXTRACT_CSV), "files_sha256": built})
        print("\nScenario files written to data/scenario/.")


def build(out_dir):
    rng = random.Random(SEED)
    reg = Registry()
    rules = load_rules()
    small, yearly = (rules["rules"]["R-SMALL-01"]["parameters"][k] for k in ("small_payment", "yearly_total"))

    clean = build_clean_ledger(read_csv(EXTRACT_CSV))
    write_csv(out_dir / "ledger_clean.csv", clean, LEDGER_FIELDS)
    ledger = [dict(r) for r in clean]
    by_id = {r["line_id"]: r for r in ledger}
    people = [r for r in ledger if r["recipient_kind"] == "person"]

    lines_of = collections.defaultdict(list)          # recipient -> lines
    for r in people:
        lines_of[(r["npi"], r["name"])].append(r)
    total_of = collections.Counter()
    for r in people:
        total_of[r["npi"]] += float(r["amount"])

    # ---- what the published records already contain (nothing planted yet)
    natural_diff, not_in_registry, clean_recipients, twins = [], [], [], []
    for key, ls in lines_of.items():
        npi, name = key
        p = reg.lookup(npi)
        if p is None:
            not_in_registry.append(key)
        elif not name_agrees_with_registry(ls[0]["first"], ls[0]["last"], p):
            natural_diff.append(key)
        else:
            clean_recipients.append(key)
            if reg.search(name, near_npi=npi)[1] > 1:
                twins.append(key)
    groups = collections.defaultdict(list)
    for r in people:
        groups[(r["npi"], r["pay_date"], r["amount"], r["nature"])].append(r["line_id"])
    natural_lookalikes = [sorted(v) for v in groups.values() if len(v) > 1]
    in_lookalike = {i for g in natural_lookalikes for i in g}

    truth, used_lines, used_recipients = [], set(), set()

    def free_lines(key):
        return [r for r in lines_of[key] if r["line_id"] not in used_lines and r["line_id"] not in in_lookalike]

    def add(kind, check, key, lines, cause, action, value, raised_by, **detail):
        truth.append({"case_id": "", "kind": kind, "split": "", "check": check, "key": key,
                      "lines": "+".join(lines), "expected_root_cause": cause, "expected_action": action,
                      "expected_value": value, "raised_by": raised_by, "detail": json.dumps(detail, sort_keys=True)})

    def take(pool, n, need_lines=1):
        """Pick n recipients not used yet that still have a free line."""
        out = []
        for key in pool:
            if len(out) == n:
                break
            if key in used_recipients or len(lines_of[key]) < need_lines or not free_lines(key):
                continue
            used_recipients.add(key)
            out.append(key)
        if len(out) < n:
            raise RuntimeError(f"wanted {n}, found {len(out)}")
        return out

    twin_pool = sorted(twins); rng.shuffle(twin_pool)
    plain_pool = sorted(k for k in clean_recipients if k not in set(twins)); rng.shuffle(plain_pool)

    # ---- A. NPI typed wrong (source error: the ledger and the filing both carry it)
    for key in take(plain_pool, N_KEYED_WRONG - N_KEYED_TWIN) + take(twin_pool, N_KEYED_TWIN, need_lines=2):
        line = rng.choice(free_lines(key)); used_lines.add(line["line_id"])
        new, how = mutate_npi(key[0], rng, reg)
        line["npi"] = new
        add("NPI_KEYED_WRONG", "IDENTITY", f'{new}|{line["name"]}', [line["line_id"]], "NPI_KEYED_WRONG", "FIX_NPI", key[0],
            "R-ID-01", how=how, twin=key in set(twins), other_lines=len(lines_of[key]) - 1)

    # ---- B. wrong person selected
    def other_people(key, same):
        first, last = lines_of[key][0]["first"], lines_of[key][0]["last"]
        cands = []
        for p in reg.people.values():
            if p["npi"] == key[0] or p["status"] != "active":
                continue
            their_first = (tokens(p["first"]) or [""])[0]
            if len(their_first) < 2:                      # skip people registered under an initial only
                continue
            lf, ll = first_names_agree(first, p["first"]), last_names_agree(last, p["last"])
            if same == "last" and ll and not lf:
                cands.append(p)
            if same == "first" and their_first == tokens(first)[0] and not ll \
                    and not name_agrees_with_registry(first, last, p):
                cands.append(p)
        return sorted(cands, key=lambda p: p["npi"])

    def plant_wrong_person(pool, n, same, need_lines=1):
        done = 0
        for key in pool:
            if done == n:
                return
            if key in used_recipients or len(lines_of[key]) < need_lines or not free_lines(key):
                continue
            cands = other_people(key, same)
            if not cands:
                continue
            used_recipients.add(key)
            p = rng.choice(cands)
            line = rng.choice(free_lines(key)); used_lines.add(line["line_id"])
            line["npi"] = p["npi"]
            add("WRONG_PERSON_SELECTED", "IDENTITY", f'{p["npi"]}|{line["name"]}', [line["line_id"]],
                "WRONG_PERSON_SELECTED", "FIX_NPI", key[0], "R-ID-02", same=same, twin=key in set(twins),
                other_lines=len(lines_of[key]) - 1, wrong_person=f'{p["first"]} {p["last"]}')
            done += 1
        if done < n:
            raise RuntimeError(f"wrong person ({same}): wanted {n}, placed {done}")

    plant_wrong_person(plain_pool, N_WRONG_SAME_LAST, "last")
    plant_wrong_person(plain_pool, N_WRONG_SAME_FIRST, "first")
    plant_wrong_person(twin_pool, N_WRONG_TWIN, "last", need_lines=3)

    # ---- C. the same-name twin: the name on the line agrees with the registry, so no rule fires
    for key in take(twin_pool, N_SILENT_TWIN):
        line = rng.choice(free_lines(key)); used_lines.add(line["line_id"])
        twin = [p for p in reg.search(key[1], near_npi=key[0], limit=50)[0] if p["npi"] != key[0]][0]
        line["npi"] = twin["npi"]
        add("SAME_NAME_TWIN", "NONE", "", [line["line_id"]], "WRONG_PERSON_SELECTED", "FIX_NPI", key[0], "none",
            twin_type=twin["type"], twin_city=twin["city"])

    # ---- D. NPI typed wrong on a recipient whose name the registry does not support: no safe correction exists
    pool = sorted(k for k in natural_diff if len(lines_of[k]) >= 2); rng.shuffle(pool)
    for key in take(pool, N_UNCONFIRMABLE, need_lines=2):
        line = rng.choice(free_lines(key)); used_lines.add(line["line_id"])
        new, how = mutate_npi(key[0], rng, reg)
        line["npi"] = new
        add("NOT_CONFIRMABLE", "IDENTITY", f'{new}|{line["name"]}', [line["line_id"]], "CANNOT_CONFIRM", "SEND_TO_PERSON", "",
            "R-ID-01", how=how, true_npi=key[0])

    # ---- E. one document loaded twice
    cands = [r for r in people if r["pay_date"][5:7] in RELOAD_MONTHS and r["line_id"] not in used_lines
             and r["line_id"] not in in_lookalike and (r["npi"], r["name"]) not in used_recipients]
    rng.shuffle(cands)
    next_id = len(ledger) + 1
    for src in cands[:N_LOADED_TWICE]:
        used_lines.add(src["line_id"])
        used_recipients.add((src["npi"], src["name"]))     # keep later plants off this recipient
        copy = dict(src, line_id=f"L{next_id:05d}", loaded_on=loaded_on(src["pay_date"], reload=True))
        next_id += 1
        ledger.append(copy); by_id[copy["line_id"]] = copy
        add("DOCUMENT_LOADED_TWICE", "LOOKALIKE", "+".join(sorted([src["line_id"], copy["line_id"]])),
            [src["line_id"], copy["line_id"]], "DOCUMENT_LOADED_TWICE", "REMOVE_LINE", copy["line_id"], "R-DUP-01",
            document=src["document"])

    # ---- what was already in the published records, with the answer the public facts support
    for key in natural_diff:
        add("NAME_DIFFERENCE_AS_PUBLISHED", "IDENTITY", f"{key[0]}|{key[1]}", [r["line_id"] for r in lines_of[key]],
            "SAME_PERSON_OTHER_NAME", "NO_CHANGE", "", "R-ID-02",
            registry_name=f'{reg.lookup(key[0])["first"]} {reg.lookup(key[0])["last"]}')
    for key in not_in_registry:
        add("NOT_IN_REGISTRY_AS_PUBLISHED", "IDENTITY", f"{key[0]}|{key[1]}", [r["line_id"] for r in lines_of[key]],
            "CANNOT_CONFIRM", "SEND_TO_PERSON", "", "R-ID-01")
    for g in natural_lookalikes:
        add("LOOKALIKE_AS_PUBLISHED", "LOOKALIKE", "+".join(g), g, "SEPARATE_PAYMENTS", "NO_CHANGE", "", "R-DUP-01")

    # ---- the draft filing, then the transfer errors (the ledger is right, the filing is not)
    filing = {r["line_id"]: {k: r[k] for k in FILING_FIELDS if k != "filing_id"} for r in ledger}

    # F. small payments left out for recipients whose yearly total requires them
    pool = sorted(k for k in clean_recipients if k not in used_recipients and total_of[k[0]] > yearly
                  and sum(1 for r in lines_of[k] if float(r["amount"]) < small and r["line_id"] not in in_lookalike) >= 3)
    rng.shuffle(pool)
    for key in pool[:N_SMALL_DROPPED]:
        used_recipients.add(key)
        dropped = [r["line_id"] for r in lines_of[key] if float(r["amount"]) < small]
        for i in dropped:
            used_lines.add(i); del filing[i]
        add("SMALL_PAYMENTS_LEFT_OUT", "RULE", key[0], dropped, "THRESHOLD_APPLIED_WITHOUT_YEARLY_TOTAL", "ADD_LINES", "",
            "R-SMALL-01", yearly_total=round(total_of[key[0]], 2))

    # G. and H. field errors on single lines
    cands = [r for r in people if r["line_id"] in filing and r["line_id"] not in used_lines
             and r["line_id"] not in in_lookalike and (r["npi"], r["name"]) not in used_recipients]
    rng.shuffle(cands)
    for src in cands[:N_AMOUNT_SWAPPED]:
        used_lines.add(src["line_id"])
        filing[src["line_id"]]["amount"] = swap_amount_digits(src["amount"], rng)
        add("AMOUNT_DIGITS_SWAPPED", "RULE", src["line_id"], [src["line_id"]], "FILING_KEYED_WRONG", "SET_FROM_LEDGER",
            src["amount"], "R-FIELD-01", filing_amount=filing[src["line_id"]]["amount"])
    for src in cands[N_AMOUNT_SWAPPED:N_AMOUNT_SWAPPED + N_YEAR_WRONG]:
        used_lines.add(src["line_id"])
        filing[src["line_id"]]["pay_date"] = "2024" + src["pay_date"][4:]
        add("YEAR_TYPED_WRONG", "RULE", src["line_id"], [src["line_id"]], "FILING_KEYED_WRONG", "SET_FROM_LEDGER",
            src["pay_date"], "R-FIELD-01", filing_date=filing[src["line_id"]]["pay_date"])

    filing_rows = []
    for n, (line_id, f) in enumerate(sorted(filing.items()), 1):
        filing_rows.append(dict(f, filing_id=f"F{n:05d}"))

    # ---- development and test split, by kind, fixed by the seed
    by_kind = collections.defaultdict(list)
    for t in truth:
        by_kind[t["kind"]].append(t)
    for kind, items in sorted(by_kind.items()):
        order = list(range(len(items))); rng.shuffle(order)
        n_dev = round(len(items) * DEV_SHARE) if len(items) > 1 else 0
        for rank, idx in enumerate(order):
            items[idx]["split"] = "dev" if rank < n_dev else "test"
    for n, t in enumerate(truth, 1):
        t["case_id"] = f"T{n:03d}"

    write_csv(out_dir / LEDGER_CSV.name, ledger, LEDGER_FIELDS)
    write_csv(out_dir / FILING_CSV.name, filing_rows, FILING_FIELDS)
    write_csv(out_dir / TRUTH_CSV.name, truth, TRUTH_FIELDS)
    # Which exceptions are for development and which for the test. Keys only, no answers:
    # this is the one scenario file besides the ledger that the agent runner reads.
    write_csv(out_dir / "splits.csv", [{"key": t["key"], "split": t["split"]} for t in truth if t["key"]], ["key", "split"])

    print(f"Ledger as published: {len(clean):,} lines, {len(lines_of)} recipients, 3 organization lines")
    print(f"Already in the published records: {len(natural_diff)} name differences, {len(not_in_registry)} NPI not in the registry, "
          f"{len(natural_lookalikes)} look-alike groups ({len(in_lookalike)} lines), {len(twins)} recipients with a same-name twin")
    print(f"Ledger with planted errors: {len(ledger):,} lines.  Draft filing: {len(filing_rows):,} lines.")
    print("\nAnswer key (data/scenario/truth.csv):")
    print(f"  {'kind':34s} {'dev':>4s} {'test':>5s}  raised by")
    for kind, items in sorted(by_kind.items()):
        print(f"  {kind:34s} {sum(t['split']=='dev' for t in items):4d} {sum(t['split']=='test' for t in items):5d}  {items[0]['raised_by']}")
    print(f"  {'total':34s} {sum(t['split']=='dev' for t in truth):4d} {sum(t['split']=='test' for t in truth):5d}")


if __name__ == "__main__":
    main()

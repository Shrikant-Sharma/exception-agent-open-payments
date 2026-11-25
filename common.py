"""Shared settings and small helpers used by every step.

Nothing in here calls a model. The name comparison and the NPI check digit
live here so that the rules, the agent's lookups and the checks all use the
same definition.
"""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
EXTRACT_DIR = DATA / "extract"
REFERENCE_DIR = DATA / "reference"
SCENARIO_DIR = DATA / "scenario"
RESULTS = ROOT / "results"
RULES_DIR = ROOT / "rules"

PROGRAM_YEAR = 2025
STATE = "NH"
# CMS dataset "2025 General Payment Data" and the reporting company whose
# records are used (the company with the most general payment records to
# New Hampshire recipients that year). The company is not the subject.
DATASET_ID = "fb0b1734-1410-429d-92f6-3f4b35218e5e"
FILER_ID = "100000000204"
SEED = 20261122

EXTRACT_CSV = EXTRACT_DIR / "general_payments_py2025.csv"
EXTRACT_MANIFEST = EXTRACT_DIR / "manifest.json"
REGISTRY_JSON = REFERENCE_DIR / "registry_snapshot.json"
REGISTRY_MANIFEST = REFERENCE_DIR / "manifest.json"
LEDGER_CSV = SCENARIO_DIR / "ledger.csv"
FILING_CSV = SCENARIO_DIR / "draft_filing.csv"
TRUTH_CSV = SCENARIO_DIR / "truth.csv"          # never read by the agent
EXCEPTIONS_CSV = RESULTS / "exception_log.csv"


# ---------------------------------------------------------------- files
def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
        f.write("\n")


def load_rules(version=None):
    """Load one version of the rule file. Default: the file for the program year."""
    version = version or f"{PROGRAM_YEAR}.1"
    return read_json(RULES_DIR / f"rules_{version}.json")


# ---------------------------------------------------------------- NPI
def npi_check_digit_ok(npi):
    """An NPI is ten digits; the last is a Luhn check digit over '80840' + the first nine."""
    if not re.fullmatch(r"\d{10}", npi or ""):
        return False
    digits = [int(c) for c in "80840" + npi]
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def digits_different(a, b):
    """How many of the ten positions differ. One wrong digit gives 1, two swapped digits give 2."""
    if len(a) != len(b):
        return max(len(a), len(b))
    return sum(1 for x, y in zip(a, b) if x != y)


# ---------------------------------------------------------------- names
def letters(s):
    return re.sub(r"[^A-Z]", "", (s or "").upper())


def tokens(s):
    return [t for t in re.split(r"[^A-Z]+", (s or "").upper()) if t]


def first_names_agree(a, b):
    """First names agree if the first words match, or one is the initial of the other,
    or they are the same letters once spaces and hyphens are removed."""
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return False
    if letters(a) == letters(b):
        return True
    x, y = ta[0], tb[0]
    if x == y:
        return True
    if len(x) == 1 or len(y) == 1:
        return x[0] == y[0]
    return False


def last_names_agree(a, b):
    """Last names agree if they are the same letters once spaces, hyphens and apostrophes are removed."""
    return bool(letters(a)) and letters(a) == letters(b)


def name_agrees_with_registry(first, last, reg):
    """Rule R-ID-02: the name on the line agrees with the registry record if it matches
    the registered name or any other name the registry lists for that person."""
    names = [(reg.get("first", ""), reg.get("last", ""))]
    names += [(o.get("first", ""), o.get("last", "")) for o in reg.get("other_names", [])]
    return any(first_names_agree(first, rf) and last_names_agree(last, rl) for rf, rl in names)


def full_name(first, middle, last, suffix=""):
    return " ".join(p for p in [first, middle, last, suffix] if p).strip()


def money(x):
    return f"${float(x):,.2f}"

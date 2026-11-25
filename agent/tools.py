"""The four lookups the agent can run. Plain code over the ledger and the registry snapshot.

Each lookup returns two things: the text the model reads, and the facts in it
as data, so the checks can later verify what the model says it saw.
None of them can read the answer key.
"""
import collections
import re

from common import digits_different, npi_check_digit_ok
from registry import Registry

LOOKUPS = ["registry_lookup", "registry_search", "ledger_history", "source_documents"]


class Lookups:
    def __init__(self, ledger, registry=None, registry_down=False):
        self.ledger = ledger
        self.by_id = {r["line_id"]: r for r in ledger}
        self.reg = registry or Registry()
        self.registry_down = registry_down          # stress test: the registry does not answer

    def run(self, name, text, case):
        """Returns (text for the model, facts as a dict)."""
        text = (text or "").strip()
        if name in ("registry_lookup", "registry_search") and self.registry_down:
            return "REGISTRY UNAVAILABLE. The lookup service did not respond.", {"failed": True}
        return getattr(self, name)(text, case)

    def registry_lookup(self, text, case):
        npi = re.sub(r"\D", "", text)
        if len(npi) != 10:
            return "Input must be one ten-digit NPI.", {"failed": True}
        p = self.reg.lookup(npi)
        if p is None:
            digit = "valid" if npi_check_digit_ok(npi) else "not valid"
            return f"NPI {npi}: no registry record. Check digit {digit}.", {"looked_up": npi, "found": False}
        return Registry.describe(p), {"looked_up": npi, "found": True, "npis": [npi]}

    def registry_search(self, text, case):
        if len(re.findall(r"[A-Za-z]+", text)) < 2:
            return "Input must be a first and last name.", {"failed": True}
        matches, total = self.reg.search(text, near_npi=case["npi"])
        name = text.upper()
        if not matches:
            return f"SEARCH FOUND NOBODY registered under the name {name}.", {"searched": name, "npis": []}
        rows, others = [], 0
        for p in matches:
            d = digits_different(p["npi"], case["npi"])
            others += d > 0
            tail = "SAME NPI AS THE LINE" if d == 0 else f"differs from the NPI on the line in {d} of 10 digits"
            rows.append(f"{Registry.describe(p)} | {tail}")
        if others == 0:
            head = f"SEARCH FOUND ONLY THE NPI ALREADY ON THE LINE under the name {name}:"
        elif others == 1 and total == 1:
            head = f"SEARCH FOUND ONE PERSON WITH A DIFFERENT NPI under the name {name}:"
        else:
            head = f"SEARCH FOUND {total} PEOPLE under the name {name}:"
        more = f"\n({total - len(matches)} more not shown)" if total > len(matches) else ""
        return head + "\n" + "\n".join(rows) + more, {"searched": name, "npis": [p["npi"] for p in matches], "total": total}

    def ledger_history(self, text, case):
        want = " ".join(text.upper().split())
        counts = collections.Counter(r["npi"] for r in self.ledger if r["recipient_kind"] == "person" and r["name"] == want)
        if not counts:
            return f"No ledger lines under the name {want}.", {"history": {}}
        parts = [f"{n} {'line carries' if n == 1 else 'lines carry'} NPI {npi}" for npi, n in counts.most_common()]
        return f"Ledger lines under the name {want}: " + "; ".join(parts) + ".", {"history": dict(counts)}

    def source_documents(self, text, case):
        ids = [i for i in dict.fromkeys(re.findall(r"L\d{5}", text.upper())) if i in self.by_id]
        if not ids:
            return "Input must be line IDs such as L00012, separated by commas.", {"failed": True}
        rows = [f'{i}: document {self.by_id[i]["document"]} | {self.by_id[i]["feed"]} | loaded {self.by_id[i]["loaded_on"]}' for i in ids]
        by_doc = collections.defaultdict(list)
        for i in ids:
            by_doc[self.by_id[i]["document"]].append(i)
        shared = [f'{" and ".join(v)} (document {d})' for d, v in by_doc.items() if len(v) > 1]
        if len(ids) < 2:
            head = ""
        elif shared:
            head = "TWO LINES SHARE A DOCUMENT NUMBER: " + "; ".join(shared) + ".\n"
        else:
            head = "ALL DOCUMENT NUMBERS ARE DIFFERENT.\n"
        return head + "\n".join(rows), {"documents": {i: self.by_id[i]["document"] for i in ids},
                                        "loaded": {i: self.by_id[i]["loaded_on"] for i in ids}}

"""The registry snapshot, with the two questions anyone asks of it:
what does the registry say about this NPI, and who is registered under this name.

Plain code, no model. The rules, the scenario builder, the agent's lookups
and the checks on the agent all go through this one class.
"""
from common import REGISTRY_JSON, digits_different, letters, read_json, tokens


class Registry:
    def __init__(self, path=REGISTRY_JSON):
        self.people = read_json(path)
        self._by_last = {}
        for p in self.people.values():
            for last in [p["last"]] + [o["last"] for o in p["other_names"]]:
                for t in set(tokens(last)) | {letters(last)}:
                    self._by_last.setdefault(t, []).append(p)

    def lookup(self, npi):
        """The registry record for an NPI, or None."""
        return self.people.get(npi)

    def search(self, name, near_npi=None, limit=5):
        """People whose registered name (or other listed name) has the same first name
        and last name as `name`. Middle names are ignored. A one-letter first name
        matches as an initial. Returns (matches, total); matches are sorted so the NPI
        closest to `near_npi` comes first."""
        t = tokens(name)
        if len(t) < 2:
            return [], 0
        first, last = t[0], t[-1]
        found = {}
        for p in self._by_last.get(last, []):
            for f, l in [(p["first"], p["last"])] + [(o["first"], o["last"]) for o in p["other_names"]]:
                ft = tokens(f)
                if not ft or not (last in tokens(l) or last == letters(l)):
                    continue
                same_first = ft[0] == first or (
                    (len(first) == 1 or len(ft[0]) == 1) and ft[0][0] == first[0])
                if same_first:
                    found[p["npi"]] = p
        out = list(found.values())
        if near_npi:
            out.sort(key=lambda p: (digits_different(p["npi"], near_npi), p["npi"]))
        else:
            out.sort(key=lambda p: p["npi"])
        return out[:limit], len(out)

    @staticmethod
    def describe(p):
        """One line of text for a registry record."""
        name = " ".join(x for x in [p["first"], p["middle"], p["last"]] if x)
        if p["credential"]:
            name += ", " + p["credential"]
        other = "; ".join(f'{o["first"]} {o["last"]}'.strip() for o in p["other_names"]) or "none"
        place = " ".join(x for x in [p["city"], p["state"]] if x) or "no location listed"
        return f'NPI {p["npi"]}: {name} | {p["type"] or "type not listed"} | {place} | {p["status"]} | other names listed: {other}'

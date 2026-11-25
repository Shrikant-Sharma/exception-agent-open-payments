"""Step 2. Take a snapshot of the reference data: the NPI registry.

Source: NPPES NPI Registry API, version 2.1 (public, no key).
Two pulls go into one snapshot:
  a. the registry record for every NPI in the payment extract
  b. every individual registered in New Hampshire who shares a last name with
     a recipient, so that a search by name returns the real list of
     look-alike people and not only the right answer

    python 02_reference.py            verify the stored snapshot against its manifest
    python 02_reference.py --refresh  pull again from the registry

The snapshot is what makes runs repeatable: the agent's lookups read this
file, not the live registry, so the same question gets the same answer.
"""
import datetime as dt
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from common import (EXTRACT_CSV, REGISTRY_JSON, REGISTRY_MANIFEST, STATE,
                    read_csv, read_json, sha256_of, write_json)

API = "https://npiregistry.cms.hhs.gov/api/"


def call(params):
    for attempt in range(4):
        try:
            r = requests.get(API, params={"version": "2.1", **params}, timeout=40)
            if r.status_code == 200:
                return r.json()
        except requests.RequestException:
            pass
        time.sleep(1 + attempt)
    raise SystemExit(f"Registry call failed: {params}")


def by_number(npi):
    return npi, call({"number": npi}).get("results", [])


def by_last_name(last):
    out, skip = [], 0
    while True:
        res = call({"last_name": last, "state": STATE, "enumeration_type": "NPI-1",
                    "limit": 200, "skip": skip}).get("results", [])
        out += res
        if len(res) < 200 or skip >= 1000:
            return last, out
        skip += 200


def slim(x):
    """Keep only what the checks and lookups use."""
    b = x.get("basic", {})
    loc = [a for a in x.get("addresses", []) if a.get("address_purpose") == "LOCATION"]
    tax = x.get("taxonomies", [])
    primary = [t for t in tax if t.get("primary")] or tax
    return {
        "npi": x["number"],
        "first": (b.get("first_name") or "").upper().strip(),
        "middle": (b.get("middle_name") or "").upper().strip(),
        "last": (b.get("last_name") or "").upper().strip(),
        "credential": (b.get("credential") or "").upper().strip(),
        "status": "active" if b.get("status") == "A" else "not active",
        "type": primary[0].get("desc", "") if primary else "",
        "city": loc[0].get("city", "").upper() if loc else "",
        "state": loc[0].get("state", "").upper() if loc else "",
        "other_names": [{"first": (o.get("first_name") or "").upper().strip(),
                         "last": (o.get("last_name") or "").upper().strip(),
                         "kind": o.get("type", "")} for o in x.get("other_names", [])],
    }


def main():
    if "--refresh" not in sys.argv and REGISTRY_JSON.exists() and REGISTRY_MANIFEST.exists():
        m = read_json(REGISTRY_MANIFEST)
        ok = sha256_of(REGISTRY_JSON) == m["sha256"]
        print(f"Stored snapshot: {m['people']:,} people pulled {m['retrieved_at_utc']}")
        print("Fingerprint matches the manifest." if ok else "FINGERPRINT DOES NOT MATCH THE MANIFEST.")
        print("Run with --refresh to pull again from the registry.")
        sys.exit(0 if ok else 1)

    rows = read_csv(EXTRACT_CSV)
    npis = sorted({r["covered_recipient_npi"] for r in rows if r["covered_recipient_npi"]})
    lasts = sorted({r["covered_recipient_last_name"].upper() for r in rows if r["covered_recipient_npi"]})
    print(f"Pulling {len(npis)} NPIs and {len(lasts)} last names from the registry...")

    people, not_found = {}, []
    with ThreadPoolExecutor(4) as ex:
        for npi, res in ex.map(by_number, npis):
            if res:
                people[npi] = slim(res[0])
            else:
                not_found.append(npi)
        n_direct = len(people)
        for last, res in ex.map(by_last_name, lasts):
            for x in res:
                people.setdefault(x["number"], slim(x))

    write_json(REGISTRY_JSON, people)
    manifest = {
        "source": "NPPES NPI Registry API, version 2.1",
        "api": API,
        "pulls": [f"number=<each of {len(npis)} NPIs in the extract>",
                  f"last_name=<each of {len(lasts)} recipient last names>, state={STATE}, enumeration_type=NPI-1"],
        "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "people": len(people),
        "recipients_found_by_npi": n_direct,
        "npis_in_extract_with_no_registry_record": not_found,
        "same_last_name_people_added": len(people) - n_direct,
        "file": REGISTRY_JSON.name,
        "sha256": sha256_of(REGISTRY_JSON),
    }
    write_json(REGISTRY_MANIFEST, manifest)
    print(f"Wrote {len(people):,} people ({n_direct} recipients, {len(not_found)} NPI with no registry record).")


if __name__ == "__main__":
    main()

"""Step 1. Pull the public payment records and write down exactly how they were pulled.

Source: CMS Open Payments, "2025 General Payment Data" (published 06/30/2026).
Scope:  every general payment one reporting company made to recipients in
        New Hampshire in program year 2025.

    python 01_extract.py            verify the stored extract against its manifest
    python 01_extract.py --refresh  pull again from CMS and rewrite both files
    python 01_extract.py --ranking  ask CMS how many records each company has for the state

The company is the one with the most such records. Its name is not kept; its
CMS ID is in the query.

The manifest is the lineage record: where the rows came from, the exact
query, when it ran, how many rows came back and the fingerprint (SHA-256)
of the file. Every later step can be traced to it.
"""
import datetime as dt
import sys

import requests

from common import (DATASET_ID, EXTRACT_CSV, EXTRACT_MANIFEST, FILER_ID, PROGRAM_YEAR, STATE,
                    read_csv, read_json, sha256_of, write_csv, write_json)

API = f"https://openpaymentsdata.cms.gov/api/1/datastore/query/{DATASET_ID}/0"
PAGE = 500

# 22 of the 91 published columns. The company name columns are left out on purpose.
KEEP = [
    "record_id", "program_year", "payment_publication_date",
    "covered_recipient_type", "covered_recipient_npi",
    "covered_recipient_first_name", "covered_recipient_middle_name",
    "covered_recipient_last_name", "covered_recipient_name_suffix",
    "teaching_hospital_name",
    "recipient_city", "recipient_state", "recipient_zip_code",
    "covered_recipient_primary_type_1", "covered_recipient_specialty_1",
    "total_amount_of_payment_usdollars", "date_of_payment",
    "form_of_payment_or_transfer_of_value", "nature_of_payment_or_transfer_of_value",
    "name_of_drug_or_biological_or_device_or_medical_supply_1",
    "city_of_travel", "state_of_travel",
]

CONDITIONS = [
    {"property": "recipient_state", "value": STATE, "operator": "="},
    {"property": "applicable_manufacturer_or_applicable_gpo_making_payment_id", "value": FILER_ID, "operator": "="},
]


def pull():
    rows, offset, total = [], 0, None
    while True:
        params = {"limit": PAGE, "offset": offset, "count": "true", "results": "true",
                  "schema": "false", "keys": "true",
                  "sorts[0][property]": "record_id", "sorts[0][order]": "asc"}
        for i, c in enumerate(CONDITIONS):
            for k, v in c.items():
                params[f"conditions[{i}][{k}]"] = v
        r = requests.get(API, params=params, timeout=120)
        r.raise_for_status()
        d = r.json()
        total = int(d["count"])
        rows += d["results"]
        print(f"  pulled {len(rows):,} of {total:,}")
        if len(d["results"]) < PAGE:
            break
        offset += PAGE
    if len(rows) != total:
        raise SystemExit(f"Row count mismatch: got {len(rows)}, the service says {total}")
    return rows


def ranking(top=5):
    """Records per reporting company for the state, largest first: why this company was chosen."""
    company = CONDITIONS[1]["property"]
    body = {"conditions": [CONDITIONS[0]],
            "properties": [company, {"expression": {"operator": "count", "operands": ["record_id"]}, "alias": "records"}],
            "groupings": [company], "sorts": [{"property": "records", "order": "desc"}],
            "limit": top, "count": False, "schema": False, "keys": True}
    r = requests.post(API, json=body, timeout=120)
    r.raise_for_status()
    return [{"company_id": x[company], "records": int(x["records"])} for x in r.json()["results"]]


def main():
    if "--ranking" in sys.argv:
        for x in ranking():
            print(f"  company ID {x['company_id']}: {x['records']:,} records" + ("   <- this project" if x["company_id"] == FILER_ID else ""))
        return
    if "--refresh" not in sys.argv and EXTRACT_CSV.exists() and EXTRACT_MANIFEST.exists():
        m = read_json(EXTRACT_MANIFEST)
        ok = sha256_of(EXTRACT_CSV) == m["sha256"] and len(read_csv(EXTRACT_CSV)) == m["rows"]
        print(f"Stored extract: {m['rows']:,} rows pulled {m['retrieved_at_utc']}")
        print("Fingerprint matches the manifest." if ok else "FINGERPRINT DOES NOT MATCH THE MANIFEST.")
        print("Run with --refresh to pull again from CMS.")
        sys.exit(0 if ok else 1)

    print("Pulling from CMS Open Payments...")
    raw = pull()
    rows = [{k: (r.get(k) or "").strip() for k in KEEP} for r in raw]
    rows.sort(key=lambda r: int(r["record_id"]))
    if len({r["record_id"] for r in rows}) != len(rows):
        raise SystemExit("Duplicate record IDs in the pull")
    write_csv(EXTRACT_CSV, rows, KEEP)
    manifest = {
        "source": "CMS Open Payments, 2025 General Payment Data",
        "dataset_id": DATASET_ID,
        "api": API,
        "conditions": CONDITIONS,
        "sorted_by": "record_id ascending",
        "program_year": PROGRAM_YEAR,
        "publication_dates_in_rows": sorted({r["payment_publication_date"] for r in rows}),
        "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rows": len(rows),
        "columns_kept": KEEP,
        "columns_published": len(raw[0]),
        "file": EXTRACT_CSV.name,
        "sha256": sha256_of(EXTRACT_CSV),
        "total_dollars": round(sum(float(r["total_amount_of_payment_usdollars"]) for r in rows), 2),
        "note": "The company name columns are not kept. The company is not the subject of this project; "
                "every error in the scenario is planted by 03_build_scenario.py.",
        "why_this_company": "It has the most 2025 general payment records for recipients in the state.",
        "records_by_company_id_top5": ranking(),
    }
    manifest["ranking_retrieved_at_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    write_json(EXTRACT_MANIFEST, manifest)
    print(f"Wrote {len(rows):,} rows, ${manifest['total_dollars']:,.2f}, sha256 {manifest['sha256'][:12]}...")


if __name__ == "__main__":
    main()

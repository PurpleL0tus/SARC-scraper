import requests
import json
import csv
import os
import time

SCHOOL_DATA = "inputs/school_list.csv"
API_BASE = "https://api.sarconline.org/api/section/print"
YEAR_ID = int(os.environ.get("YEAR_ID", 15))  # 15=2022-23, 16=2023-24, 17=2024-25
YEAR_STR = f"{YEAR_ID + 2007}-{str(YEAR_ID + 2008)[-2:]}"
JSON_DIR = f"outputs/json/{YEAR_STR}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
}


def main():
    os.makedirs(JSON_DIR, exist_ok=True)

    with open(SCHOOL_DATA, "r") as f:
        reader = csv.reader(f)
        next(reader)
        rows = list(reader)

    print(f"Total rows: {len(rows)}")

    for row in rows:
        cds_code = row[0]
        print(cds_code)

        if cds_code[-5:] == "00000":
            print("  district, skipping")
            continue

        time.sleep(2)  # DO NOT REMOVE — prevents this script from conducting a DDoS attack

        r = requests.get(f"{API_BASE}/{cds_code}/{YEAR_ID}", headers=HEADERS)

        if r.text == "Cannot view report prior to finalization":
            print("  not yet finalized, skipping")
            continue

        if len(r.content) == 0:
            print("  empty response, skipping")
            continue

        try:
            data = r.json()
        except ValueError:
            print("  invalid JSON, skipping")
            continue

        if data.get("message") == "Object reference not set to an instance of an object.":
            print("  no online SARC report filed")
            continue

        out_path = f"{JSON_DIR}/{cds_code}.json"
        with open(out_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"  saved {cds_code}.json")


if __name__ == "__main__":
    main()

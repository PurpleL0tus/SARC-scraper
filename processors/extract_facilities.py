import json
import csv
import os

SCHOOL_DATA = "inputs/school_list.csv"
YEAR_ID = int(os.environ.get("YEAR_ID", 16))  # 15=2022-23, 16=2023-24, 17=2024-25
YEAR_STR = f"{YEAR_ID + 2007}-{str(YEAR_ID + 2008)[-2:]}"
JSON_DIR = f"outputs/json/{YEAR_STR}"
OUTPUT_FILE = f"outputs/csv/facilities_data_{YEAR_STR}.csv"

FIELDS = [
    "id", "cdsCode", "yearId", "userId", "lastUpdated",
    "yearCollected", "monthCollected", "systemsStatus", "systemsText",
    "interiorStatus", "interiorText", "cleanlinessStatus", "cleanlinessText",
    "electricalStatus", "electricalText", "restroomStatus", "restroomText",
    "safetyStatus", "safetyText", "structuralStatus", "structuralText",
    "externalStatus", "externalText", "overallStatus"
]

DNE_ROW = ["SARC online DNE"] * len(FIELDS)


def clean(val):
    if val is None:
        return ""
    return str(val).replace("\n", " ").replace(",", "[insert comma]")


def extract_row(data):
    facility = data.get("facility", {}) or {}
    return [clean(facility.get(f)) for f in FIELDS]


def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(SCHOOL_DATA, "r") as f:
        rows = list(csv.reader(f))[1:]

    cds_code_errors = 0

    with open(OUTPUT_FILE, "w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["scanned_cds_code"] + FIELDS)

        for row in rows:
            cds_code = row[0]

            if cds_code[-5:] == "00000":
                print(f"{cds_code}: district, skipping")
                writer.writerow([cds_code] + DNE_ROW)
                continue

            json_path = f"{JSON_DIR}/{cds_code}.json"
            try:
                with open(json_path) as f:
                    data = json.load(f)

                json_cds = data.get("facility", {}).get("cdsCode", "")
                if json_cds != cds_code:
                    cds_code_errors += 1

                writer.writerow([cds_code] + extract_row(data))
            except FileNotFoundError:
                writer.writerow([cds_code] + DNE_ROW)

    print(f"Done. CDS code mismatches: {cds_code_errors}")


if __name__ == "__main__":
    main()

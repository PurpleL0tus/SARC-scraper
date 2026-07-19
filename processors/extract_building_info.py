import os
import re
import csv

# Extracts year built and square footage from SARC plain text files.
# Input: outputs/text/online/*.txt (produced by json_to_text.py)
# Output: outputs/csv/building_info.csv

YEAR_ID = int(os.environ.get("YEAR_ID", 16))  # 15=2022-23, 16=2023-24, 17=2024-25
YEAR_STR = f"{YEAR_ID + 2007}-{str(YEAR_ID + 2008)[-2:]}"
TEXT_DIR = f"outputs/text/online/{YEAR_STR}"
OUTPUT_FILE = f"outputs/csv/building_info_{YEAR_STR}.csv"

YEAR_BUILT_RE = re.compile(r"(?:built|founded)\s+in\s+(\d{4})", re.IGNORECASE | re.DOTALL)
SQFT_RE = re.compile(r"([\d,]{2,6})\s?(?:square|sq)\s?(?:feet|ft)", re.IGNORECASE | re.DOTALL)


def extract(content):
    years = YEAR_BUILT_RE.findall(content)
    sqfts = SQFT_RE.findall(content)
    year = min(years, key=int) if years else None
    max_sqft = max(int(s.replace(",", "")) for s in sqfts) if sqfts else None
    return year, max_sqft


def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    rows = []
    for fname in sorted(os.listdir(TEXT_DIR)):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(TEXT_DIR, fname)
        with open(path, "r", errors="replace") as f:
            content = f.read()
        year, max_sqft = extract(content)
        if year or max_sqft:
            cds_code = fname.replace(".txt", "")
            rows.append({"cds_code": cds_code, "year_built": year, "max_sqft": max_sqft})

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["cds_code", "year_built", "max_sqft"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Found building info for {len(rows)} schools → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

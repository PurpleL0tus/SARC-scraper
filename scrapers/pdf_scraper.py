import requests
import json
import csv
import os
import time

SCHOOL_DATA = "inputs/school_list.csv"
ERRORS_FILE = "outputs/errors.txt"
API_BASE = "https://api.sarconline.org/api/school"
YEAR_ID = int(os.environ.get("YEAR_ID", 15))  # 15=2022-23, 16=2023-24, 17=2024-25
YEAR_STR = f"{YEAR_ID + 2007}-{str(YEAR_ID + 2008)[-2:]}"
PDF_DIR = f"outputs/pdfs/{YEAR_STR}"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
}


def fetch_sarc_url(session, cds_code):
    r = session.get(f"{API_BASE}/{cds_code}/{YEAR_ID}", headers=HEADERS)
    if len(r.content) == 0:
        return None, "empty"
    try:
        data = json.loads(r.content)
    except json.JSONDecodeError:
        return None, "empty"
    sarc_url = data.get("sarcUrl")
    if sarc_url is None:
        return None, "null"
    if sarc_url.split(".")[-1] == "pdf":
        return sarc_url, "pdf"
    return sarc_url, "other"


def download_pdf(session, url, cds_code):
    try:
        r = session.get(url, headers=HEADERS)
        if r.status_code == 200:
            with open(f"{PDF_DIR}/{cds_code}.pdf", "wb") as f:
                f.write(r.content)
            print(f"  downloaded {cds_code}.pdf")
        else:
            print(f"  HTTP {r.status_code} for {cds_code}")
    except Exception as e:
        print(f"  failed {cds_code}: {e}")
        with open(ERRORS_FILE, "a") as f:
            f.write(cds_code + "\n")


def main():
    os.makedirs(PDF_DIR, exist_ok=True)

    with open(SCHOOL_DATA, "r") as f:
        reader = csv.reader(f)
        next(reader)
        rows = list(reader)

    print(f"Total schools: {len(rows)}")

    pdf_count = null_count = other_count = empty_count = 0

    with requests.Session() as session:
        for row in rows:
            cds_code = row[0]
            print(cds_code)

            if cds_code[-5:] == "00000":
                print("  district, skipping")
                continue

            if row[3] != "Active":
                continue

            url, status = fetch_sarc_url(session, cds_code)

            if status == "empty":
                empty_count += 1
            elif status == "null":
                null_count += 1
                print("  no sarcUrl")
            elif status == "pdf":
                pdf_count += 1
                download_pdf(session, url, cds_code)
            else:
                other_count += 1
                print(f"  non-pdf url: {url}")

            time.sleep(1.5)  # DO NOT REMOVE — prevents this script from conducting a DDoS attack

    print(f"\nPDFs: {pdf_count} | Null: {null_count} | Other: {other_count} | Empty: {empty_count}")


if __name__ == "__main__":
    main()

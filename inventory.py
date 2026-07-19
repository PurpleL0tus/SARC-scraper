import csv
import os

SCHOOL_DATA = "inputs/school_list.csv"
PDF_DIR = "outputs/pdfs"
JSON_DIR = "outputs/json"


def main():
    with open(SCHOOL_DATA, "r", encoding="utf-8", errors="replace") as f:
        rows = list(csv.reader(f))[1:]

    print("cds_code,pdf,json")
    for row in rows:
        cds_code = row[0]
        pdf_status = "exists" if os.path.exists(f"{PDF_DIR}/{cds_code}.pdf") else "missing"
        json_status = "exists" if os.path.exists(f"{JSON_DIR}/{cds_code}.json") else "missing"
        print(f"{cds_code},{pdf_status},{json_status}")


if __name__ == "__main__":
    main()

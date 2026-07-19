import csv
import os
import pdfplumber

SCHOOL_DATA = "inputs/school_list.csv"
YEAR_ID = int(os.environ.get("YEAR_ID", 16))  # 15=2022-23, 16=2023-24, 17=2024-25
YEAR_STR = f"{YEAR_ID + 2007}-{str(YEAR_ID + 2008)[-2:]}"
PDF_DIR = f"outputs/pdfs/{YEAR_STR}"
TEXT_DIR = f"outputs/text/pdf/{YEAR_STR}"


def main():
    os.makedirs(TEXT_DIR, exist_ok=True)

    with open(SCHOOL_DATA, "r", encoding="utf-8", errors="replace") as f:
        rows = list(csv.reader(f))[1:]

    count = 0
    for row in rows:
        cds_code = row[0]
        pdf_path = f"{PDF_DIR}/{cds_code}.pdf"
        txt_path = f"{TEXT_DIR}/{cds_code}.txt"

        try:
            with pdfplumber.open(pdf_path) as pdf, open(txt_path, "w", encoding="utf-8") as out:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        out.write(text + "\n")
            count += 1
            print(f"{cds_code}: extracted")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"{cds_code}: error — {e}")

    print(f"\nExtracted text from {count} PDFs")


if __name__ == "__main__":
    main()

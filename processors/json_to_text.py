import csv
import os
import re
import time

SCHOOL_DATA = "inputs/school_list.csv"
YEAR_ID = int(os.environ.get("YEAR_ID", 16))  # 15=2022-23, 16=2023-24, 17=2024-25
YEAR_STR = f"{YEAR_ID + 2007}-{str(YEAR_ID + 2008)[-2:]}"
JSON_DIR = f"outputs/json/{YEAR_STR}"
TEXT_DIR = f"outputs/text/online/{YEAR_STR}"


def clean_json_text(content):
    text = content.replace("\n", " ").replace("\\n", " ")
    text = text.replace("{", " ").replace("}", "")
    text = text.replace(":", " ").replace('"', "")
    text = text.replace("&nbsp", " ").replace("&ndash", " ")
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\$\$.*?\$\$", "", text)
    text = re.sub(r"\$[a-zA-Z0-9]\$", "", text)
    return text


def main():
    os.makedirs(TEXT_DIR, exist_ok=True)

    with open(SCHOOL_DATA, "r", encoding="utf-8", errors="replace") as f:
        rows = list(csv.reader(f))[1:]

    for row in rows:
        cds_code = row[0]
        json_path = f"{JSON_DIR}/{cds_code}.json"
        txt_path = f"{TEXT_DIR}/{cds_code}.txt"

        try:
            with open(json_path, "r") as f:
                content = f.read()

            text = clean_json_text(content)

            with open(txt_path, "w") as out:
                out.write(text)

            print(f"{cds_code}: done")
            time.sleep(0.01)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"{cds_code}: error — {e}")


if __name__ == "__main__":
    main()

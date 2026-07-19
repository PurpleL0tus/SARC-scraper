import json
import csv
import os

# Field schemas for each top-level section of the SARC online JSON response.
# Use these with extract_section() to pull any section into a CSV.

SCHOOL_FIELDS = [
    "cdsCode", "schoolName", "adminEmailAddress", "adminName", "adminPhoneNumber", "emailAddress",
    "faxNumber", "address", "city", "state", "zipCode", "district", "districtPhoneNumber",
    "districtWebsiteUrl", "superintendentFirstName", "superintendentLastName", "districtEmail",
    "yearId", "lastUpdated", "messageFromPrincipal", "schoolWebsite", "sarcUrl", "gradeLevelSpan",
    "principalPhoto", "principalComment", "charterFundCode"
]

ENROLLMENT_BY_GRADE_FIELDS = [
    "kindergarten", "grade1", "grade2", "grade3", "grade4", "grade5", "grade6", "grade7", "grade8",
    "grade9", "grade10", "grade11", "grade12", "ungradedElementary", "ungradedSecondary",
    "totalEnrollment", "lastUpdated"
]

ENROLLMENT_BY_GROUP_FIELDS = [
    "female", "male", "nonBinary", "americanIndian", "asian", "africanAmerican", "filipino",
    "hispanic", "pacificIslander", "multipleRaces", "white", "englishLearner", "fosterYouth",
    "homeless", "migrant", "socioeconomicallyDisadvantaged", "disabled", "lastUpdated"
]

CLASS_ELEMENTARY_FIELDS = [
    "avgKYear1", "avg1Year1", "avg2Year1", "avg3Year1", "avg4Year1", "avg5Year1", "avg6Year1", "avgOtherYear1",
    "ncFirstKYear1", "ncFirst1Year1", "ncFirst2Year1", "ncFirst3Year1", "ncFirst4Year1", "ncFirst5Year1", "ncFirst6Year1", "ncFirstOtherYear1",
    "ncSecondKYear1", "ncSecond1Year1", "ncSecond2Year1", "ncSecond3Year1", "ncSecond4Year1", "ncSecond5Year1", "ncSecond6Year1", "ncSecondOtherYear1",
    "ncThirdKYear1", "ncThird1Year1", "ncThird2Year1", "ncThird3Year1", "ncThird4Year1", "ncThird5Year1", "ncThird6Year1", "ncThirdOtherYear1",
    "avgKYear2", "avg1Year2", "avg2Year2", "avg3Year2", "avg4Year2", "avg5Year2", "avg6Year2", "avgOtherYear2",
    "ncFirstKYear2", "ncFirst1Year2", "ncFirst2Year2", "ncFirst3Year2", "ncFirst4Year2", "ncFirst5Year2", "ncFirst6Year2", "ncFirstOtherYear2",
    "ncSecondKYear2", "ncSecond1Year2", "ncSecond2Year2", "ncSecond3Year2", "ncSecond4Year2", "ncSecond5Year2", "ncSecond6Year2", "ncSecondOtherYear2",
    "ncThirdKYear2", "ncThird1Year2", "ncThird2Year2", "ncThird3Year2", "ncThird4Year2", "ncThird5Year2", "ncThird6Year2", "ncThirdOtherYear2",
    "avgKYear3", "avg1Year3", "avg2Year3", "avg3Year3", "avg4Year3", "avg5Year3", "avg6Year3", "avgOtherYear3",
    "ncFirstKYear3", "ncFirst1Year3", "ncFirst2Year3", "ncFirst3Year3", "ncFirst4Year3", "ncFirst5Year3", "ncFirst6Year3", "ncFirstOtherYear3",
    "ncSecondKYear3", "ncSecond1Year3", "ncSecond2Year3", "ncSecond3Year3", "ncSecond4Year3", "ncSecond5Year3", "ncSecond6Year3", "ncSecondOtherYear3",
    "ncThirdKYear3", "ncThird1Year3", "ncThird2Year3", "ncThird3Year3", "ncThird4Year3", "ncThird5Year3", "ncThird6Year3", "ncThirdOtherYear3",
    "lastUpdated"
]

CLASS_SECONDARY_FIELDS = [
    "avgEnglishYear1", "avgMathYear1", "avgScienceYear1", "avgSocialYear1",
    "ncEnglishFirstYear1", "ncMathFirstYear1", "ncScienceFirstYear1", "ncSocialFirstYear1",
    "ncEnglishSecondYear1", "ncMathSecondYear1", "ncScienceSecondYear1", "ncSocialSecondYear1",
    "ncEnglishThirdYear1", "ncMathThirdYear1", "ncScienceThirdYear1", "ncSocialThirdYear1",
    "avgEnglishYear2", "avgMathYear2", "avgScienceYear2", "avgSocialYear2",
    "ncEnglishFirstYear2", "ncMathFirstYear2", "ncScienceFirstYear2", "ncSocialFirstYear2",
    "ncEnglishSecondYear2", "ncMathSecondYear2", "ncScienceSecondYear2", "ncSocialSecondYear2",
    "ncEnglishThirdYear2", "ncMathThirdYear2", "ncScienceThirdYear2", "ncSocialThirdYear2",
    "avgEnglishYear3", "avgMathYear3", "avgScienceYear3", "avgSocialYear3",
    "ncEnglishFirstYear3", "ncMathFirstYear3", "ncScienceFirstYear3", "ncSocialFirstYear3",
    "ncEnglishSecondYear3", "ncMathSecondYear3", "ncScienceSecondYear3", "ncSocialSecondYear3",
    "ncEnglishThirdYear3", "ncMathThirdYear3", "ncScienceThirdYear3", "ncSocialThirdYear3",
    "lastUpdated"
]

SUSPENSION_FIELDS = [
    "id", "cdsCode", "yearId", "userId", "lastUpdated",
    "suspensionsYear1", "suspensionsYear2", "suspensionsYear3",
    "expulsionsYear1", "expulsionsYear2", "expulsionsYear3",
    "districtSuspensionsYear1", "districtSuspensionsYear2", "districtSuspensionsYear3",
    "districtExpulsionsYear1", "districtExpulsionsYear2", "districtExpulsionsYear3",
    "stateSuspensionsYear1", "stateSuspensionsYear2", "stateSuspensionsYear3",
    "stateExpulsionsYear1", "stateExpulsionsYear2", "stateExpulsionsYear3"
]

FACILITY_FIELDS = [
    "id", "cdsCode", "yearId", "userId", "lastUpdated",
    "yearCollected", "monthCollected", "systemsStatus", "systemsText",
    "interiorStatus", "interiorText", "cleanlinessStatus", "cleanlinessText",
    "electricalStatus", "electricalText", "restroomStatus", "restroomText",
    "safetyStatus", "safetyText", "structuralStatus", "structuralText",
    "externalStatus", "externalText", "overallStatus"
]

CREDENTIAL_FIELDS = [
    "cdsCode", "yearId", "schoolWithCredentialYear1", "schoolWithOutCredentialYear1",
    "schoolWithOutCredentialYear2", "schoolWithCredentialYear2", "schoolWithCredentialYear3",
    "schoolWithOutCredentialYear3", "districtWithOutCredentialYear3", "districtWithCredentialYear3",
    "userId", "lastUpdated", "schoolOutsideYear1", "schoolOutsideYear2", "schoolOutsideYear3",
    "districtOutsideYear3", "id"
]

SCIENCE_THREE_FIELDS = [
    "cdsCode", "yearId", "userId", "lastUpdated",
    "schoolYear2", "schoolYear3", "districtYear2", "districtYear3",
    "stateYear2", "stateYear3", "id"
]

VACANCY_FIELDS = [
    "id", "cdsCode", "yearId", "userId", "lastUpdated",
    "englishLearnersYear1", "englishLearnersYear2", "englishLearnersYear3",
    "totalMisYear1", "totalMisYear2", "totalMisYear3",
    "totalVacantYear1", "totalVacantYear2", "totalVacantYear3",
    "curriculum"
]

CURRICULUM_FIELDS = [
    "id", "cdsCode", "yearId", "userId", "lastUpdated",
    "yearCollected", "monthCollected", "readingTextbooks", "readingYearAdopted",
    "readingMostRecent", "readingPercent", "mathTextbooks", "mathYearAdopted",
    "mathMostRecent", "mathPercent", "scienceTextbooks", "scienceYearAdopted",
    "scienceMostRecent", "sciencePercent", "socialTextbooks", "socialYearAdopted",
    "socialMostRecent", "socialPercent", "foreignTextbooks", "foreignYearAdopted",
    "foreignMostRecent", "foreignPercent", "healthTextbooks", "healthYearAdopted",
    "healthMostRecent", "healthPercent", "artTextbooks", "artYearAdopted",
    "artMostRecent", "artPercent", "labPercent"
]

STAR_FIELDS = [
    "cdsCode", "schoolELAYear2", "schoolMathYear2", "schoolELAYear3", "schoolMathYear3",
    "distELAYear2", "distMathYear2", "distELAYear3", "distMathYear3",
    "stateELAYear2", "stateMathYear2", "stateELAYear3", "stateMathYear3",
    "yearId", "lastUpdated", "userId", "id"
]

# All caaspp sections (ELA grades 3-8+, Math grades 3-8+, Science) share the same field schema.
CAASPP_FIELDS = [
    "cdsCode", "yearId", "gradeId", "subject", "userId", "lastUpdated",
    "allStudentsTotalEnrollment", "allStudentsNumberTested", "allStudentsPercentTested", "allStudentsMeetExceed",
    "maleTotalEnrollment", "maleNumberTested", "malePercentTested", "maleMeetExceed",
    "femaleTotalEnrollment", "femaleNumberTested", "femalePercentTested", "femaleMeetExceed",
    "blackTotalEnrollment", "blackNumberTested", "blackPercentTested", "blackMeetExceed",
    "alaskaTotalEnrollment", "alaskaNumberTested", "alaskaPercentTested", "alaskaMeetExceed",
    "asianTotalEnrollment", "asianNumberTested", "asianPercentTested", "asianMeetExceed",
    "filipinoTotalEnrollment", "filipinoNumberTested", "filipinoPercentTested", "filipinoMeetExceed",
    "hispanicTotalEnrollment", "hispanicNumberTested", "hispanicPercentTested", "hispanicMeetExceed",
    "hawaiianTotalEnrollment", "hawaiianNumberTested", "hawaiianPercentTested", "hawaiianMeetExceed",
    "whiteTotalEnrollment", "whiteNumberTested", "whitePercentTested", "whiteMeetExceed",
    "twoTotalEnrollment", "twoNumberTested", "twoPercentTested", "twoMeetExceed",
    "disadvantagedTotalEnrollment", "disadvantagedNumberTested", "disadvantagedPercentTested", "disadvantagedMeetExceed",
    "englishLearnerTotalEnrollment", "englishLearnerNumberTested", "englishLearnerPercentTested", "englishLearnerMeetExceed",
    "disabilityTotalEnrollment", "disabilityNumberTested", "disabilityPercentTested", "disabilityMeetExceed",
    "migrantTotalEnrollment", "migrantNumberTested", "migrantPercentTested", "migrantMeetExceed",
    "fosterTotalEnrollment", "fosterNumberTested", "fosterPercentTested", "fosterMeetExceed",
    "homelessTotalEnrollment", "homelessNumberTested", "homelessPercentTested", "homelessMeetExceed",
    "allStudentsPercentNotTested", "malePercentNotTested", "femalePercentNotTested", "blackPercentNotTested",
    "alaskaPercentNotTested", "asianPercentNotTested", "filipinoPercentNotTested", "hispanicPercentNotTested",
    "hawaiianPercentNotTested", "whitePercentNotTested", "twoPercentNotTested", "disadvantagedPercentNotTested",
    "englishLearnerPercentNotTested", "disabilityPercentNotTested", "migrantPercentNotTested", "fosterPercentNotTested",
    "homelessPercentNotTested", "militaryTotalEnrollment", "militaryNumberTested", "militaryPercentTested",
    "militaryPercentNotTested", "militaryMeetExceed", "show3", "show4", "show5", "show6", "show7", "show8", "show11",
    "assessmentName"
]

# Maps section key (as it appears in the JSON) to its field list.
SECTION_FIELDS = {
    "school": SCHOOL_FIELDS,
    "enrollmentByGrade": ENROLLMENT_BY_GRADE_FIELDS,
    "enrollmentByGroup": ENROLLMENT_BY_GROUP_FIELDS,
    "classElementary": CLASS_ELEMENTARY_FIELDS,
    "classSecondary": CLASS_SECONDARY_FIELDS,
    "suspension": SUSPENSION_FIELDS,
    "facility": FACILITY_FIELDS,
    "credential": CREDENTIAL_FIELDS,
    "scienceThree": SCIENCE_THREE_FIELDS,
    "vacancy": VACANCY_FIELDS,
    "curriculum": CURRICULUM_FIELDS,
    "star": STAR_FIELDS,
    "caasppELA": CAASPP_FIELDS,
    "caasppELA1": CAASPP_FIELDS,
    "caasppELA2": CAASPP_FIELDS,
    "caasppELA3": CAASPP_FIELDS,
    "caasppELA4": CAASPP_FIELDS,
    "caasppELA5": CAASPP_FIELDS,
    "caasppELA6": CAASPP_FIELDS,
    "caasppELA7": CAASPP_FIELDS,
    "caasppMath": CAASPP_FIELDS,
    "caasppMath1": CAASPP_FIELDS,
    "caasppMath2": CAASPP_FIELDS,
    "caasppMath3": CAASPP_FIELDS,
    "caasppMath4": CAASPP_FIELDS,
    "caasppMath5": CAASPP_FIELDS,
    "caasppMath6": CAASPP_FIELDS,
    "caasppMath7": CAASPP_FIELDS,
    "caasppScience": CAASPP_FIELDS,
}


def extract_section(data, section, fields):
    section_data = data.get(section, {}) or {}
    return {f: section_data.get(f) for f in fields}


def write_section_csv(json_dir, cds_codes, section, output_path):
    fields = SECTION_FIELDS.get(section)
    if fields is None:
        raise ValueError(f"Unknown section: {section}. Valid sections: {list(SECTION_FIELDS)}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["cds_code"] + fields)
        writer.writeheader()

        for cds_code in cds_codes:
            json_path = f"{json_dir}/{cds_code}.json"
            try:
                with open(json_path) as f:
                    data = json.load(f)
                row = {"cds_code": cds_code}
                row.update(extract_section(data, section, fields))
                writer.writerow(row)
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python json_to_csv.py <section> <json_dir> <output_csv>")
        print(f"Available sections: {', '.join(SECTION_FIELDS)}")
        sys.exit(1)

    section_arg = sys.argv[1]
    json_dir_arg = sys.argv[2]
    output_arg = sys.argv[3]

    cds_list = [f.replace(".json", "") for f in os.listdir(json_dir_arg) if f.endswith(".json")]
    write_section_csv(json_dir_arg, sorted(cds_list), section_arg, output_arg)
    print(f"Wrote {output_arg}")

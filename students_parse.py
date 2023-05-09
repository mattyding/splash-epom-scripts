STUDENT_CSV = "spr23_students.csv"  # downloaded from stanfordesp`
OUTPUT_CSV = "spr23_students_parsed.csv"

EVENT_NAME = "Splash Spring 2023"

with open(STUDENT_CSV, "r") as in_f:
    next(in_f)
    lines = in_f.readlines()
    with open(OUTPUT_CSV, "w+") as out_f:
        for line in lines:
            _, first, last, student_email, dob, parent_email = line.replace(
                '"', ""
            ).split(",")
            try:
                year, month, day = dob.split("-")
            except:
                continue
            dob = f"{month}/{day}/{year}"
            email = (
                parent_email.strip()
                if (parent_email.strip() != "N/A")
                else student_email.strip()
            )
            out_f.write(f"{EVENT_NAME},{first},{last},Other,{dob},{email}\n")

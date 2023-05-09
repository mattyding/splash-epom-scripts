ePOM_CSV = "program_participants.csv"  # downloaded from ePOM
STUDENT_CSV = "students.csv"  # downloaded from stanfordesp
OUTPUT_CSV = "ePOM_parsed.csv"

with open(ePOM_CSV, "r") as in_f:
    next(in_f)
    approved_students = []
    i = 0
    for line in in_f.readlines():
        line = line.strip()
        (
            first,
            middle,
            last,
            liability,
            med_info_form,
            gender,
            parent_email,
            phone,
            dob,
        ) = line.split(",")
        liability = liability.strip('"')
        if liability == "No":
            continue
        first = first.strip('"')
        last = last.strip('"')
        approved_students.append((first, last, dob, parent_email))

    in_f.close()

print(f"There are {len(approved_students)} approved students.")

# cross-check with student CSV downloaded from stanfordesp

with open(OUTPUT_CSV, "w+") as out_f:
    out_f.write(",".join(approved_parent_emails))

print(f"Approved emails written to {OUTPUT_CSV}.")

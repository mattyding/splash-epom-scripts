TEACHER_CSV = "spr23_teachers.csv"  # downloaded from stanfordesp
OUTPUT_CSV = "spr23_teachers_parsed.csv"

EVENT_NAME = "Splash Spring 2023"

with open(TEACHER_CSV, "r") as in_f:
    next(in_f)
    lines = in_f.readlines()
    with open(OUTPUT_CSV, "w+") as out_f:
        for line in lines:
            _, first, last, email, cell = line.replace('"', "").split(",")
            sunet = email.split("@")[0]
            cell = cell if (cell.strip() != "N/A") else "650-721-4272\n"
            if email.split("@")[1] == "stanford.edu":
                out_f.write(
                    f"{EVENT_NAME},{sunet},{first},{last},Other,Volunteer,{email},{cell}"
                )
            else:
                print("Non-Stanford email found: ", first, last, email)

ePOM_CSV = "program_participants.csv"  # downloaded from ePOM
STUDENT_CSV = "spr23_students.csv"  # downloaded from stanfordesp
OUTPUT_CSV = "ePOM_parsed.csv"
CLEARED_EPOM_ENTRIES = "cleared_epom_entries.csv"


def main():
    with open(ePOM_CSV, "r") as in_f:
        next(in_f)
        epom_name_bod_set = set()
        epom_parent_email_lookup = {}
        i = 0
        for line in in_f.readlines():
            line = line.replace('"', "").strip()
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
            liability = liability.strip()
            if liability == "No":
                continue
            first = first.strip()
            last = last.strip()
            parent_email = parent_email.strip()
            epom_name_bod_set.add((first, last, dob))
            epom_parent_email_lookup[(first, last, dob)] = parent_email

        in_f.close()

    print(f"There are {len(epom_name_bod_set)} approved students.")

    # cross-check with student CSV downloaded from stanfordesp
    with open(STUDENT_CSV, "r") as in_f:
        approved_usernames = []
        matched_name_dob_set = set()
        # for finding near-matches
        website_dob_lookup = {}
        website_lookup_using_parent_email = {}

        username_lookup = {}
        get_parent_email_lookup = {}

        next(in_f)
        for line in in_f.readlines():
            _, username, first, last, student_email, dob, parent_email = line.replace(
                '"', ""
            ).split(",")
            first = first.strip()
            last = last.strip()
            parent_email = parent_email.strip()
            try:
                year, month, day = dob.split("-")
                dob = f"{month}/{day}/{year}"
            except:
                # usually skips past Harry Potter(s). Uncomment below line if you think there's an issue.
                # print(f"Cannot find a match for {first} {last} with DOB {dob}")
                continue

            # perfect match = name + dob perfectly match a record
            if (first, last, dob) in epom_name_bod_set:
                approved_usernames.append(username)
                matched_name_dob_set.add((first, last, dob))

            # for finding near-matches
            if dob not in website_dob_lookup:
                website_dob_lookup[dob] = []
            website_dob_lookup[dob].append((first, last, dob))

            if parent_email not in website_lookup_using_parent_email:
                website_lookup_using_parent_email[parent_email] = []

            username_lookup[(first, last, dob)] = username
            website_lookup_using_parent_email[parent_email].append((first, last, dob))

            get_parent_email_lookup[(first, last, dob)] = parent_email

        in_f.close()

    print(f"Perfectly matched {len(approved_usernames)} students to their usernames.")

    for non_match_student in epom_name_bod_set - matched_name_dob_set:
        nm_first, nm_last, nm_dob = non_match_student

        print(
            f"Could not find a perfect match for {nm_first} {nm_last} with DOB {nm_dob}."
        )
        # generate a list of possible matches
        poss_matches = []
        if nm_dob in website_dob_lookup:
            for same_dob in website_dob_lookup[nm_dob]:
                poss_matches.append(same_dob)
        nm_epom_parent_email = epom_parent_email_lookup[non_match_student]
        if nm_epom_parent_email in website_lookup_using_parent_email:
            for same_parent_email in website_lookup_using_parent_email[
                nm_epom_parent_email
            ]:
                poss_matches.append(same_parent_email)
        # remove duplicates
        poss_matches = list(set(poss_matches))

        # prompt user to select a match
        prompt_user(poss_matches, username_lookup, get_parent_email_lookup)
        match_indices = [int(num) for num in str(input()).split(" ")]
        # goodness checks
        while not user_input_valid(match_indices, poss_matches):
            print("Invalid input. Please try again.")
            prompt_user(poss_matches, username_lookup, get_parent_email_lookup)
            match_indices = [int(num) for num in str(input()).split(" ")]

        for match in match_indices:
            matched_username = username_lookup[poss_matches[match]]
            approved_usernames.append(matched_username)
            print(f"Matched {non_match_student} to username {matched_username}.")

    with open(OUTPUT_CSV, "w+") as out_f:
        out_f.write(",".join(set(approved_usernames)))

    print(f"Approved emails written to {OUTPUT_CSV}.")


def prompt_user(poss_matches, username_lookup, get_parent_email_lookup):
    print("Possible matches:")
    for i, match in enumerate(poss_matches):
        print(
            f"{i}: {match}, username: {username_lookup[match]}, parent email: {get_parent_email_lookup[match]}"
        )
    # add option for none
    print(f"{len(poss_matches)}: None of the above.")
    print(
        "Please select a match by entering the number. Select multiple matches by entering the numbers separated by spaces."
    )


def user_input_valid(match_indices, poss_matches):
    if len(match_indices) == 0:
        print("No match selected. Please select none of the above if you wish to skip.")
        return False
    if len(set(match_indices)) != len(match_indices):
        print(
            "Invalid input. Duplicate matches selected. Please do not select the same match twice."
        )
        return False
    if len(match_indices) > 1 and len(poss_matches) in match_indices:
        print(
            "Invalid input. You selected none of the above and another match. Please try again."
        )
        return False
    return True


if __name__ == "__main__":
    main()

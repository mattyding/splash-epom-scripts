## To get student list from website:
- Main Management Page -> Generate Printables -> Arbitrary User List
- Basic List/Students
- All students in the database -> Add Filters -> User Groups -> Select group(s) to include/Splash {EVENT} Winners
- Include only the following options and uncheck all else:
    - ID
    - First Name
    - Last Name
    - Email
    - Date of Birth
    - Guardian Email
- Select "Output type" to be CSV and download
- Copy paste to a raw .csv file.

## To transfer list of approved ePOM students to website
- ePOM -> Program Participants -> Actions -> Download -> CSV
- Move download CSV to this directory
- Run ePOM_parse.py. If it throws an error while reading the document, identify the last line in the CSV read and delete the one immediately after that. Then rerun the program.
- Process all the near-matches by typing numbers [0-9] into the terminal.
- Copy the output in ePOM_parsed.csv
- Website -> Main Management Page -> Manager User Records
- Basic List/Students
- All students in the database -> Add Filters -> User ID -> Paste -> Continue
- Student is up to date on EPOM -> Set Record(s)
- (optional) manually check all non-perfect matches
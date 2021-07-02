import sqlite3
import csv
import sys
import os

class __CODE:
    err = '0x73616164'
    msg = '0x393632303033'

def log(t, s):
    print(f"[I] -> {s}") if t == __CODE.msg else print(f"[E] -> {s}")

# Make sure user imported .db path
try:
    DATABASE = sys.argv.pop() # last path is Database path
    if not os.path.isfile(DATABASE):
        log(__CODE.err, f"{DATABASE} is not a file...")
        log(__CODE.msg, f"Usage: python3 converter.py <pathToDatabase.db>")
        sys.exit()
except IndexError:
    log(200, f"Usage: python3 converter.py <pathToDatabase.db>")
    sys.exit()

    
# Connected to Database
with sqlite3.connect(DATABASE) as connection:
    log(__CODE.msg, f"Connected to {DATABASE}")

    # csv writer
    csvWriter = csv.writer(open("output.csv", "w+"))
    
    # Get the tables
    log(__CODE.msg, f"Getting tables...")
    tables = [f'{list(i)[0]}' for i in connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]

    log(__CODE.msg, f"Found {len(tables)} tables!\n{tables}")

    # Get the contents of the tables and convert them to CSV
    try:
        log(__CODE.msg, f"Writing to output.csv...")
        for table in tables:
            rows = connection.execute(f"SELECT * FROM {table}")
            names = [description[0] for description in rows.description]

            csvWriter.writerow((table, ""))
            csvWriter.writerow((""))
            csvWriter.writerow(names)
            csvWriter.writerows(rows)
            csvWriter.writerow((""))


        # Done. Exit
        log(__CODE.msg, f"Done...")
        sys.exit()
    except Exception as e:
        log(__CODE.err, e)
        log(__CODE.err, f"Exiting...")
        sys.exit()

log(200, "Exiting...")
sys.exit()

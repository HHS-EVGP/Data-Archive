import sqlite3

dbpath = input("Enter db path: ")

# Link the database to the python cursor
con = sqlite3.connect(dbpath)
cur = con.cursor()

# Find a list of days that are present in the database
cur.execute('''
    SELECT DISTINCT
        DATE(time, 'unixepoch') AS day
        FROM main
        ORDER BY day;
''')
days = list(cur.fetchall())

## Create individual views for each existing day if they do not exist
for day in days:
    cur.execute(f"""
    CREATE VIEW IF NOT EXISTS '{day}'
    AS SELECT * FROM main
    WHERE DATE(time, 'unixepoch') = '{day}';
    """)
con.commit()

print("Views Created:", days)

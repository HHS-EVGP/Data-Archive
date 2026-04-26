# This program takes the text file that the ESP32 ouputs and converts it to a sqlite database

import sqlite3

DATALOG = "evdata.txt"
OUTPUTDB = "data.sqlite"

# Link the database to the python cursor
con = sqlite3.connect(OUTPUTDB)
cur = con.cursor()

# If main table does not exist as a table, create it
cur.execute("""
    CREATE TABLE IF NOT EXISTS main (
    time REAL UNIQUE PRIMARY KEY,
    amp_hours REAL,
    voltage REAL,
    current REAL,
    speed REAL,
    miles REAL,
    gps_fix INTEGER,
    GPS_x REAL,
    GPS_y REAL,
    throttle REAL,
    brake REAL,
    motor_temp REAL,
    batt_1 REAL,
    batt_2 REAL,
    batt_3 REAL,
    batt_4 REAL,
    ambient_temp REAL,
    rool REAL,
    pitch REAL,
    heading REAL,
    altitude REAL,
    laps NUMERIC
)
""")
con.commit()

insert_data_sql = """
    INSERT INTO main (
        time,
        amp_hours, voltage, current, speed, miles,
        gps_fix, GPS_x, GPS_y,
        throttle, brake, motor_temp, batt_1, batt_2, batt_3, batt_4,
        ambient_temp, rool, pitch, heading, altitude, laps
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, null)
    """
# laps is set to null when the data is inserted, and will be set by user input later

with open(DATALOG, "r") as file:
    for line in file:
        data = line.split(",")

        # Skip values withought timestamp
        if data[0] == 'nan':
            print("No timestamp for packet!")
            continue
        
        # Convert "nan" to none
        for i in range(len(data)):
            if data[i] == "nan":
                data[i] = None

        print(data)

        try:
            # Insert indo database
            cur.execute(insert_data_sql, data)
            con.commit()
        except Exception as e:
            print("Database Error:", e)

# Find a list of days that are present in the database
cur.execute('''
    SELECT DISTINCT
        DATE(time, 'unixepoch') AS day
        FROM main
        ORDER BY day;
''')
days = cur.fetchall()

## Create individual views for each existing day if they do not exist
for day in days:
    cur.execute(f"""
    CREATE VIEW IF NOT EXISTS '{day[0]}'
    AS SELECT * FROM main
    WHERE DATE(time, 'unixepoch') = '{day[0]}';
    """)
con.commit()
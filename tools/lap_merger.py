# This program merges lap data from the database made by the Base Station into the database from the Car

import sqlite3

BSDB = "tools/ShanendoahRaceLaps.sqlite"
CARDB = "tools/Car_051626_Shanendoah.sqlite"

laptimes = []

# Link the Base Station database
bscon = sqlite3.connect(BSDB)
bscur = bscon.cursor()

# Link the Car database
carcon = sqlite3.connect(CARDB)
carcur = carcon.cursor()

# Get a list of laps in the Base Station db
bscur.execute("""
    SELECT DISTINCT
        laps
        FROM main
""")
laps = bscur.fetchall()

# Extract values and filter out null
laps = [lap[0] for lap in laps if lap[0] is not None]

# Determine the start and end timestamps of each lap
for lap in laps:
    bscur.execute("""
        SELECT
            MAX(time), MIN(time)
            FROM main
            WHERE laps = ?
    """, [lap])
    maxtime, mintime = bscur.fetchone()
    laptimes.append((lap, mintime, maxtime))

# Update the laps field in the car db for every lap time range
for lap, mintime, maxtime in laptimes:
    carcur.execute("""
        UPDATE main
        SET laps = ?
        WHERE time BETWEEN ? AND ?
    """, (lap, mintime, maxtime))

carcon.commit()
print("Lapt data merged into", CARDB)

bscon.close()
carcon.close()

# This program requires a lot of manual control, but it lets you make custom graphs from data
# Requires pandas and plotly via pip

import sqlite3
import plotly.express as px
import pandas as pd

DBPATH = "2025-26/Car_051626_Shanendoah.sqlite"

# Define each axis
XAXIS = "GPS_x"
YAXIS = "GPS_y"
ZAXIS = "altitude"
CAXIS = "speed"
# Chose from:
# time amp_hours voltage current speed miles gps_fix GPS_x GPS_y
# throttle brake motor_temp batt_1 batt_2 batt_3 batt_4 ambient_temp
# rool pitch heading altitude laps

con = sqlite3.connect(DBPATH)

# Filter for whatever data you want
data = pd.read_sql_query(f"""
    SELECT {XAXIS}, {YAXIS}, {ZAXIS}, {CAXIS}
    FROM main
    WHERE GPS_x AND GPS_y is not 0
    AND time BETWEEN 1778951895.2 AND 1778955613.6
""", con)
# Using an f string in your query is dangerous because of SQL injection. Be careful where you use this method!!!

# Create plot from the data
fig = px.scatter_3d( # add _3d for 3d
    data,
    x=XAXIS,
    y=YAXIS,
    z=ZAXIS,
    color=CAXIS
)

# Force even axis
fig.update_layout(
    scene=dict(
        aspectmode='data'
    )
)

# Show the plot
fig.show()

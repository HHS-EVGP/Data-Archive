# Welcome to the HHS EVGP Data Archive!
This repository contains any data that we have collected and held on to from practice sessions or races using our [radio telemetry system](https://github.com/HHS-EVGP/Radio-Telemetry).

## Usage
The data is in multiple SQLite databases, grouped by date.

If you need a way to access and visualize the data, check out [DB Browser for SQLite](https://sqlitebrowser.org/).

> Note: Some of the earlier databases **may have overlapping data**, so be aware of duplicates

## Tools
We also publish any custom tools that we have created to help with analyzing our data, which can be found under [tools](https://github.com/HHS-EVGP/Data-Archive/tree/main/tools). Below is a list of what we have:
- `view_creator.py` to create views inside the database, grouping the data by day

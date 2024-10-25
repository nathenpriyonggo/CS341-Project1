# CTA L Analysis App

## Overview

This Python application provides an analysis of the Chicago Transit Authority (CTA) "L" ridership data using an SQLite database. The program fetches and analyzes data from various tables in the database and generates statistical information. Additionally, it can display data visually using matplotlib.

## Features

The application allows users to:
- View general statistics about the number of stations, stops, ridership entries, and total ridership.
- Search for stations using partial names with wildcards.
- Analyze ridership by station, including weekday, Saturday, and Sunday/holiday data.
- View the ridership on weekdays for each station, ordered by the number of riders.
- Analyze stops based on line color and direction, including accessibility information.
- Compare ridership across two different stations for a specific year.
- Plot ridership trends over time (yearly or monthly).
- Find and plot the locations of stations near a specified latitude and longitude.

## Commands

The program supports the following commands:

- `1`: Search for stations by name.
- `2`: Analyze ridership by station.
- `3`: Display ridership on weekdays for each station.
- `4`: Display stops for a specific line color and direction.
- `5`: Display the number of stops for each color by direction.
- `6`: View yearly ridership for a station.
- `7`: View monthly ridership for a station in a specific year.
- `8`: Compare ridership trends between two stations for a specific year.
- `9`: Display stations near a specific latitude and longitude and plot them on a map.
- `x`: Exit the program.

## Setup Instructions

### Prerequisites

- Python 3.x
- SQLite
- Required Python Libraries:
  - `sqlite3`
  - `matplotlib`

### Database File

Ensure that the SQLite database file (`CTA2_L_daily_ridership.db`) is located in the same directory as the Python script. If the file is too large to upload to GitHub, consider using Git LFS or providing a download link in this README file.

### Install Required Libraries

To install the required Python libraries, use the following command:

```bash
pip install matplotlib

import sqlite3
import matplotlib.pyplot as plt
import math



# ---------------------- FUNCTIONS ----------------------


# General Statistics Function
def generalStats():
    # Fetch and output number of stations
    cur.execute("""
                SELECT COUNT(*) FROM Stations;
                """)
    row = cur.fetchone()
    print("  # of stations:", row[0])

    # Fetch and output number of stops
    cur.execute("""
                SELECT COUNT(*) FROM Stops;
                """)
    row = cur.fetchone()
    print("  # of stops:", row[0])

    # Fetch and output number of ride entries
    cur.execute("""
                SELECT COUNT(*) FROM Ridership;
                """)
    row = cur.fetchone()
    print(f"  # of ride entries: {row[0]:,}")

    # Fetch and output date range
    cur.execute("""
                SELECT strftime('%Y-%m-%d', MIN(Ride_Date)),
                strftime('%Y-%m-%d', MAX(Ride_Date))
                FROM Ridership;
                """)
    row = cur.fetchone()
    print(f"  date range: {row[0]} - {row[1]}")

    # Fetch and output total ridership
    cur.execute("""
                SELECT SUM(Num_Riders) FROM Ridership;
                """)
    row = cur.fetchone()
    print(f"  Total ridership: {row[0]:,}")


# Command 1 Function
def cmd1():
    print()
    stationName = input("Enter partial station name (wildcards _ and %): ")
    # Fetch station name that contains input
    cur.execute("""
                SELECT Station_ID, Station_Name
                FROM Stations
                WHERE Station_Name LIKE ?
                ORDER BY Station_Name ASC
                """
                , [stationName])
    result = cur.fetchall()

    # Output findings
    if len(result) == 0:
        print("**No stations found...")
    else:
        for row in result:
            print(row[0], ':', row[1])


# Command 2 Function
def cmd2():
    print()
    stationName = input("Enter the name of the station you would like to analyze: ")
    # Fetch total sum of riders
    cur.execute("""
                SELECT SUM(Num_Riders)
                FROM Ridership
                JOIN Stations
                ON Ridership.Station_ID = Stations.Station_ID
                WHERE Station_Name = ?
                """
                , [stationName])
    totalRider = cur.fetchone()[0]

    # Output error message and exit if branch
    if (totalRider == None):
        print("**No data found...")

    else:
        # Fetch total sum of riders on weekdays
        cur.execute("""
                    SELECT SUM(Num_Riders)
                    FROM Ridership
                    JOIN Stations
                    ON Ridership.Station_ID = Stations.Station_ID
                    WHERE Station_Name LIKE ?
                    AND Type_of_Day LIKE 'W'
                    """
                    , [stationName])
        wkdayRider = cur.fetchone()[0]
        wkdayPercent = wkdayRider / totalRider * 100

        # Fetch total sum of riders on Saturdays
        cur.execute("""
                    SELECT SUM(Num_Riders)
                    FROM Ridership
                    JOIN Stations
                    ON Ridership.Station_ID = Stations.Station_ID
                    WHERE Station_Name LIKE ?
                    AND Type_of_Day LIKE 'A'
                    """
                    , [stationName])
        satRider = cur.fetchone()[0]
        satPercent = satRider / totalRider * 100

        # Fetch total sum of riders on Sundays
        cur.execute("""
                    SELECT SUM(Num_Riders)
                    FROM Ridership
                    JOIN Stations
                    ON Ridership.Station_ID = Stations.Station_ID
                    WHERE Station_Name LIKE ?
                    AND Type_of_Day LIKE 'U'
                    """
                    , [stationName])
        sunRider = cur.fetchone()[0]
        sunPercent = sunRider / totalRider * 100

        # Output findings
        print("Percentage of ridership for the", stationName, "station: ")
        print("  Weekday ridership:", f"{wkdayRider:,}", f"({wkdayPercent:.2f}%)")
        print("  Saturday ridership:", f"{satRider:,}", f"({satPercent:.2f}%)")
        print("  Sunday/holiday ridership:", f"{sunRider:,}", f"({sunPercent:.2f}%)")
        print("  Total ridership:", f"{totalRider:,}")


# Command 3 Function
def cmd3():
    print("Ridership on Weekdays for Each Station")
    # Fetch total sum of riders
    cur.execute("""
                SELECT SUM(Num_Riders)
                FROM Ridership
                JOIN Stations
                ON Ridership.Station_ID = Stations.Station_ID
                WHERE Type_of_Day LIKE 'W'
                """)
    totalRider = cur.fetchone()[0]
    # Fetch table of stations and their sum of riders on weekdays
    cur.execute("""
                SELECT Station_Name, SUM(Num_Riders)
                FROM Ridership
                JOIN Stations
                ON Ridership.Station_ID = Stations.Station_ID
                WHERE Type_of_Day LIKE 'W'
                GROUP BY Station_Name
                ORDER BY SUM(NUM_Riders) DESC
                """)
    res = cur.fetchall()
    
    # Loop through all stations
    for i in range(len(res)):
        percentage = res[i][1] / totalRider * 100
        # Output format
        print(res[i][0], ":", f"{res[i][1]:,}", f"({percentage:.2f}%)")


# Command 4 Function
def cmd4():
    print()
    inputColor = input("Enter a line color (e.g. Red or Yellow): ")
    # Fetch table of lines
    cur.execute("""
                SELECT Line_ID, Color
                FROM Lines
                WHERE Color LIKE ?
                """
                , [inputColor])
    res = cur.fetchone()

    # Check if line does not exist
    if (res == None):
        print("**No such line...")

    else:
        inputDirection = input("Enter a direction (N/S/W/E): ")
        cur.execute("""
                    SELECT Stop_Name, ADA
                    FROM Stops
                    JOIN StopDetails
                    ON Stops.Stop_ID = StopDetails.Stop_ID
                    WHERE Direction LIKE ?
                    AND Line_ID LIKE ?
                    ORDER BY Stop_Name ASC
                    """
                    , (inputDirection, res[0]))
        lines = cur.fetchall()
        
        # Check if line does not run in the chosen direction
        if (len(lines) == 0):
            print("**That line does not run in the direction chosen...")
        
        else:
            # Loop through all lines to output format
            for i in range(len(lines)):
                # Handicap accessible line
                if (lines[i][1] == 1):
                    print(lines[i][0], ": direction =", inputDirection.upper(), "(handicap accessible)")
                # Non-handicap accessible line
                else:
                    print(lines[i][0], ": direction =", inputDirection.upper(), "(not handicap accessible)")


# Command 5 Function
def cmd5():
    print("Number of Stops For Each Color By Direction")
    # Fetch total number of stops
    cur.execute("""
                SELECT COUNT(*)
                FROM Stops
                """)
    totalStops = cur.fetchone()[0]
    # Fetch table of line color, direction, number of stops
    cur.execute("""
                SELECT Color, Direction, COUNT(Stops.Stop_ID)
                FROM Stops
                JOIN StopDetails
                ON StopDetails.Stop_ID = Stops.Stop_ID
                JOIN Lines
                ON Lines.Line_ID = StopDetails.Line_ID
                GROUP BY Color, Direction
                ORDER BY Color ASC, Direction ASC
                """)
    res = cur.fetchall()
    # Loop through table and output format
    for i in range(len(res)):
        percentage = res[i][2] / totalStops * 100
        print(res[i][0], "going", res[i][1], ":", res[i][2], f"({percentage:.2f}%)")


# Command 6 Helper Function, Plot Construction
def cmd6PlotConstruct(res, stations):
    years = []
    riders = []

    # Fill respective x and y containers
    for row in res:
        years.append(row[0])
        riders.append(row[1])

    # Set up plot parameters
    plt.xlabel("Year")
    plt.ylabel("Number of Riders")
    plt.title(f"Yearly Ridership at {stations[0][1]} Station")
    plt.plot(years, riders)
    plt.show()


# Command 6 Function
def cmd6():
    print()
    inputStation = input("Enter a station name (wildcards _ and %): ")
    # Fetch table of station id and station name
    cur.execute("""
                SELECT Station_ID, Station_Name
                FROM Stations
                WHERE Station_Name LIKE ?
                """
                , [inputStation])
    stations = cur.fetchall()

    # Check if no stations found
    if (len(stations) == 0):
        print("**No station found...")
    # Check if multiple stations found
    elif (len(stations) > 1):
        print("**Multiple stations found...")

    else:
        # Fetch table total ridership for each year of input station
        cur.execute("""
                    SELECT strftime('%Y', Ride_Date) AS Year, SUM(Num_Riders)
                    FROM Ridership
                    WHERE Station_ID LIKE ?
                    GROUP BY Year
                    ORDER BY YEAR ASC
                    """
                    , [stations[0][0]])
        res = cur.fetchall()
        # Output format
        print("Yearly Ridership at", stations[0][1])
        for i in range(len(res)):
            print(res[i][0], ":", f"{res[i][1]:,}")

        # Prompt user if would like to plot graph
        print()
        inputPlot = input("Plot? (y/n) ")
        if (inputPlot == "y"):
            cmd6PlotConstruct(res, stations)


# Command 7 Helper Function, Plot Construction
def cmd7PlotConstruct(res, stations, inputYear):
    months = []
    riders = []

    # Fill respective x and y containers
    for row in res:
        months.append(row[0])
        riders.append(row[1])

    # Set up plot parameters
    plt.xlabel("Month")
    plt.ylabel("Number of Riders")
    plt.title(f"Monthly Ridership at {stations[0][1]} Station ({inputYear})")
    plt.ioff()
    plt.plot(months, riders)
    plt.show()


# Command 7 Function
def cmd7():
    print()
    inputStation = input("Enter a station name (wildcards _ and %): ")
    # Fetch table of station id and station name
    cur.execute("""
                SELECT Station_ID, Station_Name
                FROM Stations
                WHERE Station_Name LIKE ?
                """
                , [inputStation])
    stations = cur.fetchall()

    # Check if no stations found
    if (len(stations) == 0):
        print("**No station found...")
    # Check if multiple stations found
    elif (len(stations) > 1):
        print("**Multiple stations found...")

    else:
        inputYear = input("Enter a year: ")
        # Fetch table total ridership for each year of input station
        cur.execute("""
                    SELECT strftime('%m', Ride_Date) AS Month, SUM(Num_Riders)
                    FROM Ridership
                    WHERE Station_ID LIKE ?
                    AND strftime('%Y', Ride_Date) = ?
                    GROUP BY Month
                    ORDER BY Month ASC
                    """
                    , (stations[0][0], inputYear))
        res = cur.fetchall()
        # Output format
        print("Monthly Ridership at", stations[0][1], "for", inputYear)
        for i in range(len(res)):
            print(f"{res[i][0]}/{inputYear} :", f"{res[i][1]:,}")

        # Prompt user if would like to plot graph
        print()
        inputPlot = input("Plot? (y/n) ")
        if (inputPlot == "y"):
            cmd7PlotConstruct(res, stations, inputYear)


# Command 8 Helper Function, Plot Construction
def cmd8PlotConstruct(result1, result2, inputYear, station1, station2):
    days = list(range(1, 367))
    station1Rider = []
    station2Rider = []

    # Fill respective x and y containers
    for row in result1:
        station1Rider.append(row[1])
    for row in result2:
        station2Rider.append(row[1])

    # Set up plot parameters
    plt.xlabel("Day")
    plt.ylabel("Number of Riders")
    plt.title(f"Ridership Each Day of {inputYear}")
    plt.ioff()
    plt.plot(days, station1Rider, label=station1[0][1], color= '#1f77b4')
    plt.plot(days, station2Rider, label=station2[0][1], color='orange')
    plt.legend()
    plt.show()


# Command 8 Function
def cmd8():
    print()
    inputYear = input("Year to compare against? ")

    # Prompt user to enter first station
    print()
    inputStation1 = input("Enter station 1 (wildcards _ and %): ")
    # Fetch table of station id and station name
    cur.execute("""
                SELECT Station_ID, Station_Name 
                FROM Stations
                WHERE Station_Name LIKE ?
                """
                , [inputStation1])
    station1 = cur.fetchall()

    # Check if no stations found
    if (len(station1) == 0):
        print("**No station found...")
    # Check if multiple stations found
    elif (len(station1) > 1):
        print("**Multiple stations found...")

    else:
        # Prompt user to enter second station
        print()
        inputStation2 = input("Enter station 2 (wildcards _ and %): ")
        # Fetch table of station id and station name
        cur.execute("""
                    SELECT Station_ID, Station_Name 
                    FROM Stations
                    WHERE Station_Name LIKE ?
                    """
                    , [inputStation2])
        station2 = cur.fetchall()

        # Check if no stations found
        if (len(station2) == 0):
            print("**No station found...")
        # Check if multiple stations found
        elif (len(station2) > 1):
            print("**Multiple stations found...")

        else:
            # Fetch table of date and total ridership for station 1
            cur.execute("""
                        SELECT strftime('%Y-%m-%d', Ride_Date) AS Date, SUM(Num_Riders)
                        FROM Ridership
                        WHERE Station_ID LIKE ?
                        AND strftime('%Y', Ride_Date) = ?
                        GROUP BY Date
                        ORDER BY Date ASC
                        """
                        , (station1[0][0], inputYear))
            result1 = cur.fetchall()

            # Print station 1 header
            print("Station 1:", station1[0][0], station1[0][1])
            # Loop through station 1 table and output first 5
            for i in range(5):
                if (len(result1) != 0):
                    print(result1[i][0], result1[i][1])
            # Loop through station 1 table and output last 5
            for i in range(-5, 0, 1):
                if (len(result1) != 0):
                    print(result1[i][0], result1[i][1])

            # Fetch table of date and total ridership for station 2
            cur.execute("""
                        SELECT strftime('%Y-%m-%d', Ride_Date) AS Date, SUM(Num_Riders)
                        FROM Ridership
                        WHERE Station_ID LIKE ?
                        AND strftime('%Y', Ride_Date) = ?
                        GROUP BY Date
                        ORDER BY Date ASC
                        """
                        , (station2[0][0], inputYear))
            result2 = cur.fetchall()

            # Print station 2 header
            print("Station 2:", station2[0][0], station2[0][1])
            # Loop through station 2 table and output first 2
            for i in range(5):
                if (len(result2) != 0):
                    print(result2[i][0], result2[i][1])
            # Loop through station 2 table and output last 2
            for i in range(-5, 0, 1):
                if (len(result2) != 0):
                    print(result2[i][0], result2[i][1])

            # Prompt user if would like to plot graph
            print()
            inputPlot = input("Plot? (y/n) ")
            if (inputPlot == "y"):
                cmd8PlotConstruct(result1, result2, inputYear, station1, station2)


# Command 9 Helper Function, Plot Construction
def cmd9PlotConstruct(res):
    #
    # populate x and y lists with (x, y) coordinates
    # note that longitude are the X values and
    # latitude are the Y values
    #
    x = []
    y = []
    for row in res:
        x.append(row[2])
        y.append(row[1])
    
    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868] # area covered by the map

    plt.imshow(image, extent=xydims)
    plt.title("Stations Near You")
    plt.plot(x, y)
    #
    # annotate each (x, y) coordinate with its station name:
    #
    for row in res:
        plt.annotate(row[0], (row[2], row[1]))

    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])
    plt.show()


# Command 9 Function
def cmd9():
    print()
    # Prompt user for latitude
    lat = float(input("Enter a latitude: "))
    
    if lat < 40 or lat > 43:
        print("**Latitude entered is out of bounds...")
    else:
        # Prompt user for longitude
        lon = float(input("Enter a longitude: "))
        
        if lon < -88 or lon > -87:
            print("**Longitude entered is out of bounds...")
        
        else:
            # Calculate mile radius bounds and round values
            lat_min = lat - round(1 / 69, 3)
            lat_max = lat + round(1 / 69, 3)
            lon_min = lon - round(1 / 51, 3)
            lon_max = lon + round(1 / 51, 3)

            # Fetch table of stations with coordinates in mile radius
            cur.execute("""
                        SELECT DISTINCT Station_Name, Latitude, Longitude
                        FROM Stops
                        LEFT JOIN Stations
                        ON Stops.Station_ID = Stations.Station_ID
                        WHERE Latitude BETWEEN ? AND ?
                        AND Longitude BETWEEN ? AND ?
                        ORDER BY Station_Name
                        """
                        , (lat_min, lat_max, lon_min, lon_max))
            res = cur.fetchall()

            # Check if no stations found
            if (len(res) == 0):
                print("**No stations found...")
            else:
                print()
                print("List of Stations Within a Mile")
                # Loop through table to print output format
                for i in range(len(res)):
                    print(f"{res[i][0]} : ({res[i][1]}, {res[i][2]})")
                
                # Prompt user if would like to plot graph
                print()
                inputPlot = input("Plot? (y/n) ")
                if (inputPlot == "y"):
                    cmd9PlotConstruct(res)



# ---------------------- END OF FUNCTIONS ---------------------- 



# Open database connection
con = sqlite3.connect("CTA2_L_daily_ridership.db")
cur = con.cursor()

# Output welcome message and statistics title
print("** Welcome to CTA L analysis app **")
print()
print("General Statistics:")
generalStats()
print()

# Start command-loop
cmd = input("Please enter a command (1-9, x to exit): ")
while cmd != 'x':

    # Command 1
    if cmd == '1': 
        cmd1()

    # Command 2
    elif cmd == '2':
        cmd2()      

    # Command 3
    elif cmd == '3':
        cmd3()            

    # Command 4
    elif cmd == '4':
        cmd4()

    # Command 5
    elif cmd == '5':
        cmd5()

    # Command 6
    elif cmd == '6':
        cmd6()

    # Command 7
    elif cmd == '7':
        cmd7()

    # Command 8
    elif cmd == '8':
        cmd8()

    # Command 9
    elif cmd == '9':
        cmd9()

    # Error message
    else:
        print("**Error, unknown command, try again...")
    
    # Prompt user to repeat command loop
    print()
    cmd = input("Please enter a command (1-9, x to exit): ")
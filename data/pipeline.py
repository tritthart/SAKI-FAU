import sqlite3
import datetime
import utils

from data_sources import BicycleDataSource, WeatherDataSource
from db_manager import DBManager

# Config
path = "./data/data.sqlite"
bicycleURL = "https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_DATE.csv.gz"
weatherURL = "https://bulk.meteostat.net/v2/daily/STATION.csv.gz"
blacklistedStations = {100013034, 100012161, 100048814, 100036542}


def importBicycleData(db, cycleDS):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    for city in cycleDS.data[0][["standort"]].groupby("standort"):
        db.addCity(cursor, city[0])
    for city in cycleDS.data[0].groupby("counter_site"):
        if int(city[1].iloc[0]["counter_site_id"]) in blacklistedStations:
            continue
        cursor.execute(
            """
			SELECT id FROM city
			WHERE name LIKE ?
		""",
            (city[1].iloc[0]["standort"],),
        )

        db.addBicycleStation(
            cursor,
            city[0],
            cursor.fetchone()[0],
            city[1].iloc[0]["longitude"],
            city[1].iloc[0]["latitude"],
        )

    nameToStationID = {}
    cursor.execute(
        """
			SELECT id, name FROM bicycle_station
		"""
    )
    for station in cursor.fetchall():
        nameToStationID[station[1]] = station[0]

    for monthlyEntry in cycleDS.data:
        dateString = datetime.datetime.strptime(
            monthlyEntry.iloc[0]["timestamp"], "%Y-%m-%dT%H:%M:%S%z"
        ).strftime("%B, %Y")
        print(f"Importing bicycle data for {dateString}")
        utils.clear()
        for i, entry in monthlyEntry.iterrows():
            if (
                int(entry["counter_site_id"]) in blacklistedStations
                or entry["counter_site"] not in nameToStationID
            ):
                blacklistedStations.add(int(entry["counter_site_id"]))
                continue
            db.addBicycleCount(
                cursor,
                nameToStationID[entry["counter_site"]],
                entry["timestamp"],
                entry["zählstand"],
            )

    print(f"Blacklisted stations: {blacklistedStations}")

    conn.commit()
    conn.close()


def importWeatherData(db, weatherDSs):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    for weatherDS in weatherDSs:
        print(f"Importing weather data for {weatherDS.city}")
        utils.clear()
        cursor.execute(
            """
			SELECT id FROM city
			WHERE name LIKE ?
		""",
            (weatherDS.city,),
        )
        weatherStationID = db.addWeatherStation(cursor, cursor.fetchone()[0])
        for i, entry in weatherDS.data.iterrows():
            db.addWeatherEntry(
                cursor,
                weatherStationID,
                entry["date"],
                entry["tavg"],
                entry["tmin"],
                entry["tmax"],
                entry["prcp"],
                entry["snow"],
                entry["wdir"],
                entry["wspd"],
                entry["wpgt"],
                entry["pres"],
                entry["tsun"],
            )

    conn.commit()
    conn.close()


def startPipeline():
    db = DBManager(path)
    cycleDS = BicycleDataSource(bicycleURL, datetime.date(2021, 1, 1))
    weatherDSs = []
    print("Fetching bicycle data:")
    cycleDS.fetchData()
    utils.clear()
    for city in cycleDS.data[0][["standort"]].groupby("standort"):
        print(f"Fetching weather data for {city[0]}")
        utils.clear()
        weatherDSs.append(WeatherDataSource(weatherURL, city[0]))
    [weatherDS.fetchData() for weatherDS in weatherDSs]

    db.rebuildDB()
    importBicycleData(db, cycleDS)
    importWeatherData(db, weatherDSs)
    print("Done!")


if __name__ == "__main__":
    startPipeline()

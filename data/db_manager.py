import sqlite3
import os

from pathlib import Path


class DBManager:
    def __init__(self, path: str):
        self.path = path

    def createDB(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS city (
				id INTEGER PRIMARY KEY,
				name TEXT NOT NULL
			)
		"""
        )
        cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS bicycle_station (
				id INTEGER PRIMARY KEY,
				name TEXT NOT NULL,
				city_id INTEGER NOT NULL,
				longitude TEXT NOT NULL,
				latitude TEXT NOT NULL
			)
		"""
        )
        cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS bicycle_count (
				id INTEGER PRIMARY KEY,
				bicycle_station_id INTEGER NOT NULL,
				timestamp TEXT NOT NULL,
				count TEXT NOT NULL
			)
		"""
        )
        cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS weather_station (
				id INTEGER PRIMARY KEY,
				city_id INTEGER NOT NULL
			)
		"""
        )
        cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS weather_entry (
				id INTEGER PRIMARY KEY,
				weather_station_id INTEGER NOT NULL,
				date TEXT,
				tavg REAL,
				tmin REAL,
				tmax REAL,
				prcp REAL,
				snow INTEGER,
				wdir INTEGER,
				wspd REAL,
				wpgt REAL,
				pres REAL,
				tsun INTEGER
			)
		"""
        )

        conn.commit()
        conn.close()

    def rebuildDB(self):
        if Path(self.path).exists():
            os.remove(self.path)
        self.createDB()

    def addCity(self, cursor, city):
        cursor.execute(
            """
			INSERT INTO city (name)
			VALUES (?)
		""",
            (city,),
        )

    def addBicycleStation(self, cursor, name, cityID, longitude, latitude):
        cursor.execute(
            """
			INSERT INTO bicycle_station (name, city_id, longitude, latitude)
			VALUES (?, ?, ?, ?)
		""",
            (name, cityID, longitude, latitude),
        )

    def addBicycleCount(self, cursor, bicycleStationID, timestamp, count):
        cursor.execute(
            """
			INSERT INTO bicycle_count (bicycle_station_id, timestamp, count)
			VALUES (?, ?, ?)
		""",
            (bicycleStationID, timestamp, count),
        )

    def addWeatherStation(self, cursor, cityID):
        cursor.execute(
            """
			INSERT INTO weather_station (city_id)
			VALUES (?)
		""",
            (cityID,),
        )
        return cursor.lastrowid

    def addWeatherEntry(
        self,
        cursor,
        weather_station_id,
        date,
        tavg,
        tmin,
        tmax,
        prcp,
        snow,
        wdir,
        wspd,
        wpgt,
        pres,
        tsun,
    ):
        cursor.execute(
            """
			INSERT INTO weather_entry (
				weather_station_id, date, tavg, tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		""",
            (
                weather_station_id,
                date,
                tavg,
                tmin,
                tmax,
                prcp,
                snow,
                wdir,
                wspd,
                wpgt,
                pres,
                tsun,
            ),
        )

import requests
import gzip
import datetime
import pandas as pd
import utils

from io import StringIO
from dateutil.rrule import rrule, MONTHLY


class BicycleDataSource:
    def __init__(self, url: str, startDate: datetime):
        self.url = url
        self.startDate = startDate
        self.data = []

    def fetchData(self):
        dates = list(
            rrule(freq=MONTHLY, dtstart=self.startDate, until=datetime.datetime.now())
        )
        for d in dates:
            url = self.url.replace("DATE", d.strftime("%Y%m"))
            print(f"Fetching data for {d.strftime('%B, %Y')}")
            utils.clear()
            r = None
            try:
                r = requests.get(url)
            except:
                raise ValueError("Pipeline failed to fetch data")
            if r == None or r.status_code != 200:
                raise ValueError(f"Pipeline failed to fetch data")
                break
            rawData = gzip.decompress(r.content)
            self.data.append(pd.read_csv(StringIO(rawData.decode("utf-8"))))


class WeatherDataSource:
    stations = {
        "Konstanz": "10929",
        "Stuttgart": "10739",
        "Heilbronn": "10756",
        "Lörrach": "EDTR0",
        "Böblingen": "D4160",
        "Tübingen": "D4294",
        "Reutlingen": "D3278",
        "Singen": "D6263",
        "Ulm": "10838",
        "Ludwisburg": "10739",
        "Offenburg": "D1089",
        "Heidelberg": "10734",
        "Freiburg": "10803",
    }

    def __init__(self, url: str, city: str):
        self.url = url
        self.data = None
        self.city = city
        if city in self.stations:
            self.station = self.stations[city]
        else:
            for station in self.stations:
                if station in city:
                    self.station = self.stations[station]
                    return
            raise ValueError(f"Error: could not find weather station for {city}")

    def fetchData(self):
        url = self.url.replace("STATION", self.station)
        r = None
        try:
            r = requests.get(url)
        except:
            raise ValueError("Pipeline failed to fetch data")
        if r == None or r.status_code != 200:
            raise ValueError(f"Pipeline failed to fetch data")
        rawData = gzip.decompress(r.content)
        self.data = pd.read_csv(StringIO(rawData.decode("utf-8")))
        self.data.columns = [
            "date",
            "tavg",
            "tmin",
            "tmax",
            "prcp",
            "snow",
            "wdir",
            "wspd",
            "wpgt",
            "pres",
            "tsun",
        ]

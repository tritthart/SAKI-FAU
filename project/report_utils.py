import sqlalchemy as sql
import pandas as pd
import numpy as np
from IPython.display import HTML

### All functions and variables defined in here are extracted from the report to make the report easier to read.


## Collecting all required data from the database
def fetchData():
    engine = sql.create_engine("sqlite:///./data/data.sqlite")
    with engine.connect() as conn:
        startDate = "2021-01-01"
        ## Bicycle
        # Fetch data from the db
        df_cities = pd.read_sql("SELECT * FROM city", conn)
        df_bicycleStation = pd.read_sql("SELECT * FROM bicycle_station", conn)
        df_bicycleCount = pd.read_sql("SELECT * FROM bicycle_count", conn)

        # Form the data
        df_bicycleCount["timestamp"] = pd.to_datetime(df_bicycleCount["timestamp"]).dt.tz_convert(None)
        df_bicycleCount["count"] = df_bicycleCount["count"].astype(int)
        df_bicycleCount = df_bicycleCount.loc[df_bicycleCount["timestamp"] >= startDate]

        # Merge the data
        df = df_bicycleCount.merge(df_bicycleStation, left_on="bicycle_station_id", right_on="id", how="right").merge(df_cities, left_on="city_id", right_on="id", how="right")
        df.set_index("timestamp", inplace=True)

        # Group the data by station
        groupedBicycleByStation = df.groupby("bicycle_station_id")

        ## Weather
        # Fetch data from the db
        df_cities = pd.read_sql("SELECT * FROM city", conn)
        df_weatherStation = pd.read_sql("SELECT * FROM weather_station", conn)
        df_weatherEntry = pd.read_sql("SELECT * FROM weather_entry", conn)

        # Form the data
        df_weatherEntry["date"] = pd.to_datetime(df_weatherEntry["date"])
        df_weatherEntry = df_weatherEntry.loc[df_weatherEntry["date"] >= startDate]

        # Merge the data
        df = df_weatherEntry.merge(df_weatherStation, left_on="weather_station_id", right_on="id", how="right").merge(df_cities, left_on="city_id", right_on="id", how="right")
        df.set_index("date", inplace=True)

        # Group the data by station
        groupedWeatherByCity = df.groupby("city_id")

    return (groupedBicycleByStation, groupedWeatherByCity)


## Creating weekly and daily dfs for each weather station merged with bicycle counting stations
def prepareData(groupedBicycleByStation, groupedWeatherByCity):
    stationBicycleWeeklies = []
    stationBicycleDailies = []
    cityWeatherWeeklies = []

    for resolution, stationBicycleResolution, stationWeatherResolution in [
        ("W", stationBicycleWeeklies, cityWeatherWeeklies),
        ("D", stationBicycleDailies, []),
    ]:
        for city, df_cityWeather in groupedWeatherByCity:
            df_cityWeather = df_cityWeather.resample(resolution).agg(
                {
                    "tavg": "mean",
                    "tmin": "min",
                    "tmax": "max",
                    "prcp": "mean",
                    "snow": "mean",
                    "wdir": "mean",
                    "wspd": "mean",
                    "wpgt": "mean",
                    "pres": "mean",
                    "tsun": "mean",
                    "name": "first",
                    "city_id": "first",
                }
            )
            df_cityWeather.reset_index(inplace=True)
            df_cityWeather["date"] = pd.to_datetime(df_cityWeather["date"])
            stationWeatherResolution.append(df_cityWeather)

        for station, df_station in groupedBicycleByStation:
            df_station = df_station.resample(resolution).agg(
                {
                    "count": "sum",
                    "bicycle_station_id": "first",
                    "name_y": "first",
                    "name_x": "first",
                    "city_id": "first",
                }
            )
            df_station.reset_index(inplace=True)
            j = 0

            # Matching weather data to station
            for city in stationWeatherResolution:
                if df_station["city_id"].iloc[0] == city["city_id"].iloc[0]:
                    df_weather_weekly = city
                    break
                j += 1
            df_station = df_station.merge(
                stationWeatherResolution[j],
                left_on="timestamp",
                right_on="date",
                how="left",
            )
            # Add day of week
            df_station["day_of_week"] = df_station["timestamp"].dt.dayofweek + 1
            df_station["month"] = df_station["timestamp"].dt.month
            df_station["year"] = df_station["timestamp"].dt.year
            stationBicycleResolution.append(df_station)

    dfAllWeekly = pd.concat(stationBicycleWeeklies)
    dfAllDaily = pd.concat(stationBicycleDailies)

    return (
        stationBicycleWeeklies,
        stationBicycleDailies,
        cityWeatherWeeklies,
        dfAllWeekly,
        dfAllDaily,
    )


## Helper function for function below
def aggWeightedMean(df, column):
    return (df[column] * df["count"]).sum() / df["count"].sum()


## Calculates correlation for cities, summarizes counting stations by calculation a weighted average
def addCorrelation(df):
    stationNames = []
    cityNames = []
    columns = ["station_id"]

    for weatherType in weatherTypes:
        columns.append(f"{weatherType}_corr")
    dfCorr = pd.DataFrame(columns=columns)

    for city_df in df:
        stationNames.append(city_df["name_x"].iloc[0])
        cityNames.append(city_df["name_y"].iloc[0])
        new_row = pd.DataFrame({"station_id": [city_df["bicycle_station_id"].iloc[0]]})
        for weatherType in weatherTypes:
            correlation = city_df["count"].corr(city_df[weatherType])
            new_row[f"{weatherType}_corr"] = correlation
        dfCorr = pd.concat([dfCorr, new_row], ignore_index=True)
    cityNames = list(dict.fromkeys(cityNames))

    df = pd.concat(df).merge(dfCorr, left_on="bicycle_station_id", right_on="station_id", how="left")
    results = {}
    for column in columns[1:]:
        results[column] = df.groupby("city_id_y").apply(aggWeightedMean, column=column)
        results[column] = results[column].apply(lambda x: np.nan if x == 0 else x)
    return (pd.DataFrame(results), cityNames)


## Used to build custom subplots
def buildHTMLPlot():
    html = """
		<style>
		table, tr, td {
			background-color: white;
		}
		</style>
		'<table>'
		
		"""
    for i in range(2):
        html += "<tr>"
        for j in range(3):
            html += f'<td><img src="./data/figures/{weatherTypesSmall[i*3+j]}.png"></td>'
        html += "</tr>"
    html += "</table>"
    return HTML(html)


## Some definitions to make everything easier
weatherTypes = ["tavg", "tmax", "tmin", "tsun", "pres", "prcp", "wpgt", "snow", "wspd"]
weatherTypesSmall = ["tavg", "wspd", "tsun", "pres", "wdir", "prcp"]

weatherDict = {
    "prcp": "Precipitation",
    "wspd": "Wind speed",
    "tavg": "Average temperature",
    "wdir": "Wind direction",
    "wpgt": "Peak gust",
    "pres": "Pressure",
    "tsun": "Sunshine",
    "tmax": "Maximum temperature",
    "tmin": "Minimum temperature",
    "snow": "Snow",
}
weatherDictUnit = {
    "prcp": "Precipitation (mm)",
    "wspd": "Wind speed (m/s)",
    "tavg": "Average temperature (°C)",
    "wdir": "Wind direction (°)",
    "wpgt": "Peak gust (m/s)",
    "pres": "Pressure (hPa)",
    "tsun": "Sunshine (hours)",
}
weatherTypes = ["tavg", "tmax", "tmin", "tsun", "pres", "prcp", "wpgt", "snow", "wspd"]

# Sourced from:
# https://fahrradklima-test.adfc.de/fileadmin/BV/FKT/Download-Material/Ergebnisse_2022/ADFC-Fahrradklima-Test_2022_Ergebnistabelle_Druck_Gesamt_A3_230404.pdf
rank = {
    "Stadt Ludwigsburg": 3.64,
    "Landeshauptstadt Stuttgart": 4.2,
    "Stadt Heidelberg": 3.64,
    "Stadt Lörrach": 3.77,
    "Stadt Ulm": 3.96,
    "Stadt Freiburg": 3.11,
    "Stadt Konstanz": 3.27,
    "Stadt Tübingen": 3.12,
    "Landkreis Böblingen": 3.7,
    "Stadt Heilbronn": 3.82,
}

import urllib.request
import zipfile
import pandas as pd
import sqlalchemy as sql
import os

res = urllib.request.urlretrieve("https://gtfs.rhoenenergie-bus.de/GTFS.zip")


with zipfile.ZipFile(res[0], "r") as zip_file:
    zip_file.extract("stops.txt")

df = pd.read_csv(
    "stops.txt",
    sep=",",
    encoding="utf-8",
    usecols=["stop_id", "stop_name", "stop_lat", "stop_lon", "zone_id"],
    dtype={"stop_id": int, "stop_name": str,"stop_lat": float, "stop_lon": float, "zone_id": int}
).dropna()

os.remove("stops.txt")

df = df[df["zone_id"] == 2001]
df = df[(df["stop_lat"] <= 90) & (df["stop_lat"] >= -90)]
df = df[(df["stop_lon"] <= 90) & (df["stop_lon"] >= -90)]

engine = sql.create_engine("sqlite:///gtfs.sqlite")
df.to_sql(
    "stops",
    engine,
    if_exists="replace",
    index=False,
)
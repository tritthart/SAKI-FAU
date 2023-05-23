import pandas as pd
import sqlalchemy as sql

url = "https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv"
df = pd.read_csv(url, delimiter=';')
engine = sql.create_engine("sqlite:///airports.sqlite")
airportModel = {
    "column_1": sql.types.Integer,
    "column_2": sql.types.String,
    "column_3": sql.types.String,
    "column_4": sql.types.String,
    "column_5": sql.types.String,
    "column_6": sql.types.String,
    "column_7": sql.types.Float,
    "column_8": sql.types.Float,
    "column_9": sql.types.Integer,
    "column_10": sql.types.Float,
    "column_11": sql.types.String,
    "column_12": sql.types.String,
    "geo_punkt": sql.types.String
}
df.to_sql("airports", engine, if_exists="replace", index=False, dtype=airportModel)
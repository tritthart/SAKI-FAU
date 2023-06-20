import pandas as pd
import sqlalchemy as sql

url = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv"

# Creating a dataframe
df = pd.read_csv(
    url,
    delimiter=";",
    encoding="cp1252",
    skiprows=6,
    skipfooter=4,
    header=0,
    na_values="-",
    engine="python",
    names=[
        "date",
        "CIN",
        "name",
        "petrol",
        "diesel",
        "gas",
        "electro",
        "hybrid",
        "plugInHybrid",
        "others",
    ],
    usecols=[
        ord(x[-1]) - ord("A") + 1 + (ord(x[0]) - (ord("A")) + 1) * 26 * (len(x) - 1) - 1
        for x in ["A", "B", "C", "M", "W", "AG", "AQ", "BA", "BK", "BU"]
    ],
    dtype={"CIN": str},
).dropna()

# Constraints
df = df[(df["CIN"].str.len() == 5) & (df["CIN"].str.isdigit())]
df = df[
    (df["petrol"] > 0)
    & (df["diesel"] > 0)
    & (df["gas"] > 0)
    & (df["electro"] > 0)
    & (df["hybrid"] > 0)
    & (df["plugInHybrid"] > 0)
    & (df["others"] > 0)
]

# Creating the db
engine = sql.create_engine("sqlite:///cars.sqlite")
df.to_sql(
    "cars",
    engine,
    if_exists="replace",
    index=False,
    dtype={
        "date": sql.types.String,
        "CIN": sql.types.String,
        "name": sql.types.String,
        "petrol": sql.types.Integer,
        "diesel": sql.types.Integer,
        "gas": sql.types.Integer,
        "electro": sql.types.Integer,
        "hybrid": sql.types.Integer,
        "plugInHybrid": sql.types.Integer,
        "others": sql.types.Integer,
    },
)

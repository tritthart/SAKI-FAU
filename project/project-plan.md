# Project Plan

## Summary

<!-- Describe your data science project in max. 5 sentences. -->
This project analyzes bicycle traffic in 13 cities and communes across Baden-Württemberg in relation to recorded local weather data. The goal is to visualize a correlation (should it exist) between different weather conditions to the daily popularity of bicycling.
### Research Question
Which effects have certain weather conditions on the frequency of bicycle traffic?
## Rationale

<!-- Outline the impact of the analysis, e.g. which pains it solves. -->
The analysis helps policymakers to see current pain points caused by weather that hamper the popularity of sustainable transport. 
By analyzing usage patterns, city planners can improve road infrastructure against certain weather conditions to promote cycling.
Through continuous integration of new data, policymakers can review real-world effects of infrastructure changes by comparing current bicycle frequencies to historic ones under different weather conditions.
## Data Sources

<!-- Describe each data sources you plan to use in a section. Use the prefix "DatasourceX" where X is the id of the data source. -->

### Datasource1: Consolidated Eco-counter Bicycle Count Data for Baden-Württemberg
* Metadata URL: https://mobilithek.info/offers/-5646868446023868292
* Data URLs: 
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202101.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202102.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202103.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202104.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202105.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202106.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202107.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202108.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202109.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202110.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202111.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202112.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202201.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202202.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202203.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202204.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202205.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202206.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202207.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202208.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202209.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202210.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202211.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202212.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202301.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202302.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202303.csv.gz
https://mobidata-bw.de/daten/eco-counter/eco_counter_fahrradzaehler_202304.csv.gz
* Data Type: CSV

Daily bicycle frequencies of 13 cities and communes across Baden-Württemberg, 
collected from automated counting stations, spread around cities, from Jan. 2021, updated weekly.

### Datasource2: Daily Station Observations of Multiple Weather Parameters
* Metadata URL: https://dev.meteostat.net/bulk/daily.html
* Data URLs:
https://bulk.meteostat.net/v2/daily/10929.csv.gz (Konstanz)
https://bulk.meteostat.net/v2/daily/10739.csv.gz (Stuttgart)
https://bulk.meteostat.net/v2/daily/10756.csv.gz (Heilbronn)
https://bulk.meteostat.net/v2/daily/EDTR0.csv.gz (Lörrach)
https://bulk.meteostat.net/v2/daily/D4160.csv.gz (Böblingen)
https://bulk.meteostat.net/v2/daily/D4294.csv.gz (Tübingen)
https://bulk.meteostat.net/v2/daily/D3278.csv.gz (Reutlingen)
https://bulk.meteostat.net/v2/daily/D6263.csv.gz (Singen)
https://bulk.meteostat.net/v2/daily/10838.csv.gz (Ulm)
https://bulk.meteostat.net/v2/daily/10739.csv.gz (Ludwigsburg)
https://bulk.meteostat.net/v2/daily/D1089.csv.gz (Offenburg)
https://bulk.meteostat.net/v2/daily/10734.csv.gz (Heidelberg)
https://bulk.meteostat.net/v2/daily/10803.csv.gz (Freiburg)
* Data Type: CSV

Records of daily weather parameters(temperature, precipitation, snowfall, sunshine duration) of 13 locations which occur in Datasource1. 
## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Fetch the latest data from sources [#1][i1]
2. Prepare weather data for analysis [#2][i2]
3. Prepare bicycling data for analysis [#3][i3]
4. CD: set up a pipeline for continuous integration of new data [#4][i4]
5. Review if there are missing data in the historical weather records [#5][i5]
6. Visualize the integrated dataset to gain insights into the relationship between weather conditions and bicycle traffic [#6][i6]


[i1]: https://github.com/jvalue/2023-amse-template/issues/1
[i2]: https://github.com/jvalue/2023-amse-template/issues/2
[i3]: https://github.com/jvalue/2023-amse-template/issues/3
[i4]: https://github.com/jvalue/2023-amse-template/issues/4
[i5]: https://github.com/jvalue/2023-amse-template/issues/5
[i6]: https://github.com/jvalue/2023-amse-template/issues/6

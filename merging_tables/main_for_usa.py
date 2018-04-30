import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from pytz import timezone
from bisect import bisect_left


metar_table = pd.read_csv("metar_table_usa_3_airports.csv", index_col=[0, 1], parse_dates=[1])
metar_table = metar_table[~metar_table.index.duplicated(keep='first')]

airports_list = ["ATL", "JFK", "LAS"]

from_airport_to_available_metar_timestamps = {}

for airport in airports_list:
    from_airport_to_available_metar_timestamps[airport] = sorted(list(metar_table.loc[airport].index))

# for airport in airports_list:
#     from_airport_to_available_metar_timestamps[airport] = np.sort(np.array(metar_table.loc[airport].index))


dataset = pd.read_csv("LAS-JFK-ATL-utc-preprocessed.csv",
                      index_col=0,
                      parse_dates=["SCH_START_DATETIME", "SCH_END_DATETIME", "ACT_START_DATETIME", "ACT_END_DATETIME"])

dataset = dataset[(dataset.Origin == "ATL") | (dataset.Origin == "JFK") | (dataset.Origin == "LAS")]


def get_last_metar_datetime(row: pd.Series):
    ind = max(bisect_left(from_airport_to_available_metar_timestamps[row["Origin"]],
                       row["SCH_START_DATETIME"] + timedelta(minutes=10)) - 1, 0)
    return from_airport_to_available_metar_timestamps[row["Origin"]][ind]


dataset["LAST_METAR_REPORT_TIME"] = dataset.apply(get_last_metar_datetime, axis=1)

merged = dataset.join(metar_table, on=["Origin", "LAST_METAR_REPORT_TIME"])

merged.drop(["code", "mod", "additional_vis", "additional_vis_dir", "wind_dir_from", "wind_dir_to",
             "sky_conditions", "present_weather"], axis=1, inplace=True)

columns = merged.columns
weather_cond_columns = columns[66:]

merged[weather_cond_columns] = merged[weather_cond_columns].astype(np.byte)

merged.to_hdf("dataset_with_weather.hdf5", key="data")

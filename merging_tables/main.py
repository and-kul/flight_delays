import pandas as pd
import numpy as np
from datetime import datetime
import pytz
from pytz import timezone

utc = pytz.utc
moscow_tz = timezone('Europe/Moscow')


def round_down_to_nearest_30_minutes(timestamp: datetime):
    return datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour,
                    (timestamp.minute // 30) * 30)


def from_moscow_to_utc(timestamp):
    try:
        moscow_time = moscow_tz.localize(timestamp)
        utc_time = moscow_time.astimezone(utc)
        return utc_time
    except:
        return np.datetime64('NaT')


def mark_as_utc(timestamp):
    return utc.localize(timestamp)



date_columns_ids = [1, 2, 8, 9, 10, 11, 12, 13, 14, 15]
flight_leg_exp: pd.DataFrame = pd.read_excel('flight_leg_exp.xlsx', parse_dates=date_columns_ids)
print("loaded")

date_columns_names = flight_leg_exp.columns[date_columns_ids]

# # todo: remove
# flight_leg_exp = flight_leg_exp.iloc[:100000]

for column_name in date_columns_names:
    # flight_leg_exp[column_name] = flight_leg_exp[column_name].apply(from_moscow_to_utc)
    flight_leg_exp[column_name] = flight_leg_exp[column_name].apply(mark_as_utc)
    print(column_name)

metar_table = pd.read_csv("metar_table_v0.3.csv", index_col=0, parse_dates=True)
metar_table.index = metar_table.index.map(mark_as_utc)


flight_leg_exp["IS_FROM_SVO"] = flight_leg_exp["PUB_DEPARTURE_AIRPORT_CODE"] == "SVO"

flight_leg_exp["LAST_METAR_REPORT_TIME"] = flight_leg_exp["SCH_START_DATE_TIME"]\
    .apply(round_down_to_nearest_30_minutes)\
    .apply(mark_as_utc)

merged = flight_leg_exp.join(metar_table, on="LAST_METAR_REPORT_TIME")

merged.to_csv("flight_leg_exp_joined_with_metar_flight_time_treated_as_utc.csv", index=False)

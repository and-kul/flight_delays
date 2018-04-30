import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_hdf("dataset_with_weather.hdf5", key="data")
dataset.reset_index(inplace=True)

dataset["dep_delay_more_15"] = dataset.DepDelayMinutes >= 15

dataset = dataset[["Quarter", "Month", "DayofMonth", "DayOfWeek", "AirlineID", "Origin", "TIME_FROM_LAST_FACT_LAND",
                   "LATE_ARRIVAL_BEFORE", "FLIGHT_TIME_TO_MIDNIGHT", "wind_speed_mps", "wind_gust_mps", "wind_dir",
                   "vis", "runway_visual_range_from", "first_layer_coverage", "first_layer_height", "first_layer_CB",
                   "first_layer_TCU", "clouds_hidden", "vertical_visibility", "heavy thunderstorm with rain and hail",
                   "patches of fog", "nearby fog", "ice pellets and rain", "dust", "rain and ice pellets",
                   "blowing snow", "light freezing rain, snow and ice pellets", "snow pellets", "snow", "drizzle",
                   "ice pellets and snow", "light freezing rain and snow", "nearby blowing dust", "light rain",
                   "heavy rain and ice pellets", "smoke", "heavy thunderstorm with rain", "squalls",
                   "thunderstorm with snow pellets and rain", "light rain and ice pellets",
                   "heavy thunderstorm with rain and snow pellets", "light ice pellets and snow", "light drizzle",
                   "light freezing rain", "light ice pellets, snow and rain", "thunderstorm",
                   "light freezing rain and ice pellets", "haze", "mist", "thunderstorm with rain", "light snow",
                   "rain, snow and ice pellets", "shallow fog", "light freezing rain, ice pellets and snow",
                   "nearby thunderstorm", "rain and snow", "light snow and ice pellets",
                   "light rain, snow and ice pellets", "unknown precipitation", "light thunderstorm with rain and snow",
                   "light thunderstorm with rain", "light freezing drizzle", "light rain, ice pellets and snow",
                   "light snow and rain", "freezing rain and ice pellets", "heavy ice pellets and snow", "blowing dust",
                   "heavy rain", "ice pellets", "freezing rain", "freezing fog", "light ice pellets, rain and snow",
                   "fog", "rain", "heavy snow", "nearby dust", "light snow, rain and ice pellets",
                   "light rain and snow", "light ice pellets and rain", "light ice pellets", "dep_delay_more_15"
                   ]]

dataset[["Quarter", "Month", "DayofMonth", "DayOfWeek"]] = \
    dataset[["Quarter", "Month", "DayofMonth", "DayOfWeek"]].astype(np.int8)

dataset[["AirlineID"]] = \
    dataset[["AirlineID"]].astype(np.int32)

dataset[["TIME_FROM_LAST_FACT_LAND", "LATE_ARRIVAL_BEFORE"]] = \
    dataset[["TIME_FROM_LAST_FACT_LAND", "LATE_ARRIVAL_BEFORE"]].astype(np.int32)

dataset[["FLIGHT_TIME_TO_MIDNIGHT"]] = \
    dataset[["FLIGHT_TIME_TO_MIDNIGHT"]].astype(np.int8)

dataset[["first_layer_coverage", "first_layer_CB", "first_layer_TCU", "clouds_hidden"]] = \
    dataset[["first_layer_coverage", "first_layer_CB", "first_layer_TCU", "clouds_hidden"]].astype(np.int8)

dataset.to_hdf("dataset_for_prediction.hdf5", key="data")

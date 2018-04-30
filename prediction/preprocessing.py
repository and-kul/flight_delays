import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy.stats import mode
import collections

dataset = pd.read_hdf("dataset_for_prediction.hdf5", key="data")

# Preprocessing:


airlines_label_encoder = preprocessing.LabelEncoder()
dataset["AirlineID"] = airlines_label_encoder.fit_transform(dataset["AirlineID"])

dataset.wind_speed_mps.fillna(0, inplace=True)
dataset.wind_gust_mps.fillna(0, inplace=True)


#  Replacing NaN values of wind_dir with the most frequent for current airport
x = dataset[["Origin", "wind_dir"]]
x = x.groupby("Origin").agg({"wind_dir": lambda wind_dir: mode(wind_dir.dropna())[0][0]})\
    .rename(columns={"wind_dir": "airport_wind_dir_mode"})
x = dataset.join(x, on="Origin")["airport_wind_dir_mode"]
dataset.wind_dir.fillna(x, inplace=True)


max_vis = dataset.vis.max()
dataset.vis.fillna(max_vis, inplace=True)

dataset.runway_visual_range_from.fillna(max_vis, inplace=True)

dataset.to_hdf("dataset_for_prediction_preprocessed.hdf5", key="data")

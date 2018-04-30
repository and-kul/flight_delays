import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_hdf("dataset_with_weather.hdf5", key="data")

dataset["dep_delay_more_15"] = dataset.DepDelayMinutes >= 15

df1 = dataset[["Origin", "Year", "dep_delay_more_15"]]
df2 = df1.groupby("Origin").agg({"Year": "count", "dep_delay_more_15": "sum"}) \
    .rename(columns={"Year": "total_flights", "dep_delay_more_15": "with_delay"})

df2["without_delay"] = df2.total_flights - df2.with_delay
df2["delay_fraction"] = df2.with_delay / df2.total_flights

plt.figure(figsize=(8, 6))
ind = np.arange(3)
width = 0.35

p1 = plt.bar(ind, df2.with_delay, width)
p2 = plt.bar(ind, df2.without_delay, width, bottom=df2.with_delay)

plt.ylabel('Flights')
plt.title('Departure delays 2012-2016')
plt.xticks(ind, df2.index)
plt.yticks(np.arange(0, 2000000, 100000))
plt.legend((p1[0], p2[0]), ('With delay (15 min)', 'Without delay'))

plt.show()

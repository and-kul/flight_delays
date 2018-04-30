import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy.stats import mode
import collections
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, recall_score, precision_score
from imblearn.over_sampling import SMOTE

dataset = pd.read_hdf("dataset_for_prediction_preprocessed.hdf5", key="data")


for_stratify = dataset.Origin.map(str).add(dataset.dep_delay_more_15.astype(np.int8).apply(str))



# Preprocessing:

airports_label_encoder = preprocessing.LabelEncoder()
dataset["Origin"] = airports_label_encoder.fit_transform(dataset["Origin"])

X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

smote = SMOTE(n_jobs=-1)
X, y = smote.fit_sample(X, y)





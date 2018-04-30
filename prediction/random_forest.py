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

dataset = pd.read_hdf("dataset_for_prediction_preprocessed.hdf5", key="data")


for_stratify = dataset.Origin.map(str).add(dataset.dep_delay_more_15.astype(np.int8).apply(str))



# Preprocessing:

airports_label_encoder = preprocessing.LabelEncoder()
dataset["Origin"] = airports_label_encoder.fit_transform(dataset["Origin"])

X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=for_stratify)


# RandomForest

clf = RandomForestClassifier(n_estimators=100,
                             max_depth=10,
                             n_jobs=-1,
                             class_weight='balanced_subsample',
                             random_state=0)


start_time = time.time()
clf.fit(X_train, y_train)
print('classifier training time: %3.2f minutes' % ((time.time() - start_time) / 60))

y_pred = clf.predict(X_test)


print('accuracy score: %2.3f' % accuracy_score(y_test, y_pred))
print('precision score: %2.3f' % precision_score(y_test, y_pred))
print('recall score: %2.3f' % recall_score(y_test, y_pred))
print('f1 score: %2.3f' % f1_score(y_test, y_pred))



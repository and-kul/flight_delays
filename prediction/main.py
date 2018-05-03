import lightgbm as lgb
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn import preprocessing
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score
from sklearn.model_selection import train_test_split

dataset = pd.read_hdf("dataset_for_prediction_preprocessed.hdf5", key="data")


for_stratify = dataset.Origin.map(str).add(dataset.dep_delay_more_15.astype(np.int8).apply(str))



# Preprocessing:

airports_label_encoder = preprocessing.LabelEncoder()
dataset["Origin"] = airports_label_encoder.fit_transform(dataset["Origin"])

X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

smote = SMOTE(n_jobs=-1)
X, y = smote.fit_sample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
gbm = lgb.LGBMClassifier(num_leaves=31,
                         n_estimators=100,
                         max_depth=-1,
                         objective="binary",
                         random_state=0,
                         silent=False)
gbm.fit(X_train,
        y_train)

y_pred = gbm.predict(X_test)
print('accuracy score: %2.3f' % accuracy_score(y_test, y_pred))
print('precision score: %2.3f' % precision_score(y_test, y_pred))
print('recall score: %2.3f' % recall_score(y_test, y_pred))
print('f1 score: %2.3f' % f1_score(y_test, y_pred))


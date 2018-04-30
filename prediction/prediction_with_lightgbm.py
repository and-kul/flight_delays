import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=for_stratify)

gbm = lgb.LGBMClassifier(num_leaves=63,
                         n_estimators=200,
                         max_depth=-1,
                         class_weight="balanced",
                         objective="binary",
                         random_state=0,
                         silent=False)

gbm.fit(X_train,
        y_train,
        categorical_feature=
        ["Quarter", "Month", "DayofMonth", "DayOfWeek", "AirlineID", "Origin", "first_layer_CB",
         "first_layer_TCU", "clouds_hidden",
         "heavy thunderstorm with rain and hail",
         "patches of fog", "nearby fog", "ice pellets and rain", "dust",
         "rain and ice pellets",
         "blowing snow", "light freezing rain, snow and ice pellets",
         "snow pellets", "snow", "drizzle",
         "ice pellets and snow", "light freezing rain and snow",
         "nearby blowing dust", "light rain",
         "heavy rain and ice pellets", "smoke", "heavy thunderstorm with rain",
         "squalls", "thunderstorm with snow pellets and rain",
         "light rain and ice pellets",
         "heavy thunderstorm with rain and snow pellets",
         "light ice pellets and snow", "light drizzle",
         "light freezing rain", "light ice pellets, snow and rain", "thunderstorm",
         "light freezing rain and ice pellets", "haze", "mist",
         "thunderstorm with rain", "light snow",
         "rain, snow and ice pellets", "shallow fog",
         "light freezing rain, ice pellets and snow",
         "nearby thunderstorm", "rain and snow", "light snow and ice pellets",
         "light rain, snow and ice pellets", "unknown precipitation",
         "light thunderstorm with rain and snow",
         "light thunderstorm with rain", "light freezing drizzle",
         "light rain, ice pellets and snow",
         "light snow and rain", "freezing rain and ice pellets",
         "heavy ice pellets and snow", "blowing dust",
         "heavy rain", "ice pellets", "freezing rain", "freezing fog",
         "light ice pellets, rain and snow",
         "fog", "rain", "heavy snow", "nearby dust",
         "light snow, rain and ice pellets",
         "light rain and snow", "light ice pellets and rain", "light ice pellets",
         ],
        verbose=True)


y_pred = gbm.predict(X_test)


print('accuracy score: %2.3f' % accuracy_score(y_test, y_pred))
print('precision score: %2.3f' % precision_score(y_test, y_pred))
print('recall score: %2.3f' % recall_score(y_test, y_pred))
print('f1 score: %2.3f' % f1_score(y_test, y_pred))

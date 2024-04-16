from adtk.data import validate_series
from adtk.detector import ThresholdAD
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def anomaly_detection(dataset, high, low, column):
    data = dataset.loc[:, ["TimeStamp",
                           column]]
    data = data.set_index("TimeStamp")
    data.index = pd.to_datetime(data.index)
    data = validate_series(data)
    threshold_ad = ThresholdAD(high=high, low=low)
    anomalies = threshold_ad.detect(data)
    data["Anomaly"] = anomalies.values
    data["Anomaly"] = pd.get_dummies(data["Anomaly"], drop_first=True)

    return data["Anomaly"].values


def anomaly_detection_manual(data, column, high, low):
    data_true = data.loc[(data[column] > high) | (data[column] < low)]
    index = data_true.index.values

    return index

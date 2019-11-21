from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
import numpy, pandas
import get_dataset
from matplotlib import pyplot as plt
from sklearn.feature_selection import SelectKBest, chi2
from scipy.stats import pearsonr
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import os.path
import process_output, calc_corr

dir_prefix = "./processed_data/"
result_dir_prefix = "./result_data/"

csv_arr = ["activity", "audio", "bluetooth", "dark", "phonecharge", "phonelock", "wifi", "conversation",
           "wifi_location", "gps"]

label_dict = {
    "phonelock": ["phonelock duration during morning", "phonelock duration during afternoon",
                  "phonelock duration during evening",
                  "phonelock duration during night"],
    "phonecharge": ["phonecharge duration during morning", "phonecharge duration during afternoon",
                    "phonecharge duration during evening",
                    "phonecharge duration during night"],
    "dark": ["light duration during morning", "light duration during afternoon", "light duration during evening",
             "light duration during night"],
    "gps": ["network times of gps provider", "gps times of gps provider", "wifi times of gps_network_type",
            "cell times of gps_network_type", "average accuracy", "average bearing", "average speed"
            ],
    "wifi_location": ["the frequency of changing building", "average frequency of changing building"],
    "bluetooth": ["total counts of bluetooth mac address", "bluetooth class", "high strength of bluetooth level",
                  "medium strength of bluetooth level", "low strength of bluetooth level"],
    "wifi": ["total counts of wifi-bssid address", "frequency of wifi", "high strength of wifi level",
             "medium strength of wifi level", "low strength of wifi level"],
    "activity": ["activity_0 times count", "daily average activity_0 count", "daily average activity_0 ratio",
                 "activity_1 times count", "daily average activity_1 times", "daily average activity_1 ratio",
                 "activity_2 times count", "daily average activity_2 times", "daily average activity_2 ratio",
                 "activity_3 times count", "daily average activity_3 count",
                 "daily average activity_3 ratio",
                 "daily average activity_0 count during day", "daily average activity_0 ratio during day",
                 "daily average activity_1 times during day", "daily average activity_1 ratio during day",
                 "daily average activity_2 times during day", "daily average activity_2 ratio during day",
                 "daily average activity_3 times during day", "daily average activity_3 ratio during day",
                 "daily average activity_0 count during night", "daily average activity_0 ratio during night",
                 "daily average activity_1 times during night", "daily average activity_1 ratio during night",
                 "daily average activity_2 times during night", "daily average activity_2 ratio during night",
                 "daily average activity_3 times during night",
                 "daily average activity_3 ratio during night",
                 ],
    "audio": ["audio_0 times count", "daily average audio_0 count", "daily average audio_0 ratio",
              "audio_1 times count", "daily average audio_1 times", "daily average audio_1 ratio",
              "audio_2 times count", "daily average audio_2 times", "daily average audio_2 ratio",
              "daily average audio_0 count during day", "daily average audio_0 ratio during day",
              "daily average audio_1 times during day", "daily average audio_1 ratio during day",
              "daily average audio_2 times during day", "daily average audio_2 ratio during day",
              "daily average audio_0 count during night", "daily average audio_0 ratio during night",
              "daily average audio_1 times during night", "daily average audio_1 ratio during night",
              "daily average audio_2 times during night", "daily average audio_2 ratio during night",
              ],
    "conversation": ["daily frequency of conversation", "daily average conversation duration",
                     "average duration of each conversation", "daily frequency of long-time conversation(>10 mins)",
                     "daily average long-time conversation duration(>10 mins)",
                     "average duration of each long-time conversation(>10 mins)",
                     "daily frequency of conversation during day",
                     "daily average conversation duration during day",
                     "average duration of each conversation during day",
                     "daily frequency of conversation during night",
                     "daily average conversation duration during night",
                     "average duration of each conversation during night",
                     ],
}


def match_feature_label(key, index):
    try:
        # print(key,index)
        return label_dict[key][index].capitalize()
    except KeyError or IndexError:
        return key + "_" + str(index)

label_of_importance = []

memory_dict={"arr":label_of_importance,"dfs":0}

def get_data_sets(threshold=0):
    global memory_dict
    if memory_dict["dfs"] !=0:
        return memory_dict["dfs"]

    out_dict = process_output.get_output_dict("val")
    out_df = pandas.DataFrame(out_dict).T
    dfs = {}
    out_labels = ["FlourishingScale", "Positive", "Negative"]
    out_df.columns = out_labels
    tmp_labels = out_labels.copy()
    for label in out_labels:
        if os.path.isfile(result_dir_prefix + label + "_" + str(threshold) + ".csv"):
            dfs[label] = pandas.read_csv(result_dir_prefix + label + "_" + str(threshold) + ".csv", index_col=0)
            tmp_labels.remove(label)
        else:
            dfs[label] = out_df[[label]]
    out_labels = tmp_labels
    if len(out_labels) < 1:
        return dfs
    for csv_index in range(len(csv_arr)):
        csv_file = dir_prefix + csv_arr[csv_index] + ".csv"
        df = pandas.read_csv(csv_file)
        in_dict = df.to_dict("list")
        features = calc_corr.get_corr_with_threshold(in_dict, out_dict, threshold=threshold)
        in_df = df.T
        for label in out_labels:
            if len(features[label]) < 1:
                continue
            tmp_df = in_df[features[label]]
            tmp_df.columns = [match_feature_label(csv_arr[csv_index], i) for i in features[label]]
            dfs[label] = pandas.merge(dfs[label], tmp_df, left_index=True, right_index=True)

    for label in out_labels:
        df = dfs[label]
        df.to_csv(result_dir_prefix + label + "_" + str(threshold) + ".csv")
    memory_dict["dfs"]=dfs
    return dfs



def feature_select(x, y, labels, importance=30):
    global memory_dict
    label_of_importance=memory_dict["arr"]
    if len(label_of_importance) > importance:
        return label_of_importance[:importance]
    scaling = StandardScaler()
    scaling.fit(x)
    x = scaling.transform(x)

    forest = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1,
                                    max_depth=15)
    forest.fit(x, y)

    importances = forest.feature_importances_
    indices = numpy.argsort(importances)[::-1]

    memory_dict["arr"] = [labels[indices[i]] for i in range(0, len(labels))]
    return label_of_importance[:importance]


def get_k_features_by_importance(k=30):
    if k == 0:
        k = 30
    dfs = {}
    out_labels = ["FlourishingScale", "Positive", "Negative"]
    tmp_labels = out_labels.copy()
    for label in out_labels:
        if os.path.isfile(result_dir_prefix + label + "_k" + str(k) + ".csv"):
            dfs[label] = pandas.read_csv(result_dir_prefix + label + "_k" + str(k) + ".csv", index_col=0)
            tmp_labels.remove(label)
    if len(tmp_labels) < 1:
        return dfs
    dfs = get_data_sets(threshold=0)
    for label in out_labels:
        df = dfs[label]
        # transfer the output values from Numeric to Class (0-> LOW , 1-> HIGH) using median
        y_median = df[label].median()
        df.loc[df[label] <= y_median, label] = 0
        df.loc[df[label] > y_median, label] = 1
        x = df.drop(columns=label)
        labels = x.columns
        y = df[label].to_numpy()
        labels = feature_select(x, y, labels, importance=k)
        labels.append(label)
        dfs[label] = df[labels]
    for label in out_labels:
        df = dfs[label]
        df.to_csv(result_dir_prefix + label + "_k" + str(k) + ".csv")
    return dfs


if __name__ == "__main__":
    print(get_data_sets())

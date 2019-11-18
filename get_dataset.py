import process_output, calc_corr
import csv
import pandas
import os

dir_prefix = "./processed_data/"
csv_arr = ["activity", "audio", "bluetooth", "dark", "phonecharge", "phonelock", "wifi", "conversation"]


def get_data_sets(threshold=0.1):
    out_dict = process_output.get_output_dict("val")
    out_df = pandas.DataFrame(out_dict).T
    dfs = {}
    out_labels = ["FlourishingScale", "Positive", "Negative"]
    out_df.columns = out_labels
    tmp_labels = out_labels.copy()
    for label in out_labels:
        if os.path.isfile(dir_prefix + label + "_" + str(threshold) + ".csv"):
            dfs[label] = pandas.read_csv(dir_prefix + label + "_" + str(threshold) + ".csv", index_col=0)
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
        features = calc_corr.get_corr_with_threshold(in_dict, out_dict,threshold=threshold)
        in_df = df.T
        for label in out_labels:
            if len(features[label]) < 1:
                continue
            tmp_df = in_df[features[label]]
            tmp_df.columns = [csv_arr[csv_index] + "_" + str(i) for i in features[label]]
            dfs[label] = pandas.merge(dfs[label], tmp_df, left_index=True, right_index=True)

    for label in out_labels:
        df = dfs[label]
        # df.to_csv(dir_prefix+label+"_"+str(threshold)+".csv")
    return dfs


if __name__ == "__main__":
    print(get_data_sets())

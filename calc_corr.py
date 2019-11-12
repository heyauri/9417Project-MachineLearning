import process_output
import process_input
import pandas
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def concat_dicts_by_uid(in_dict, out_dict):
    result = {}
    for uid in out_dict:
        result[uid] = in_dict[uid] + out_dict[uid]
    return result


def get_corr(in_dict,heatmap=False):
    output = process_output.get_output_dict(1)
    d = concat_dicts_by_uid(in_dict, output)
    df=pandas.DataFrame(d).T
    labels=list(df)
    labels=labels[:-3]
    for i in range(0,len(labels)):
        labels[i]="X"+str(labels[i])
    labels=labels+["Flourishing Scale","Positive","Negative"]

    df.columns=labels

    print(df)
    if heatmap:
        plt.figure(figsize=(12, 10))
        cor = df.corr()
        sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
        plt.show()


if __name__ == "__main__":
    # print(fs_df)
    # print(ps_df)
    # data=get_output_value()
    # pandas.set_option('display.max_rows', data.shape[0] + 1)
    # print(data)
    activities = process_input.get_activity_data()
    get_corr(activities)

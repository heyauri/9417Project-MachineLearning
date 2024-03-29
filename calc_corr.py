import process_output
import process_input
import pandas
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import random

sns.set(font_scale=1.5)

def concat_dicts_by_uid(in_dict, out_dict):
    result = {}
    for uid in out_dict:
        result[uid] = in_dict[uid] + out_dict[uid]
    return result

#if needed, use PCA for decomposition
def input_pca(in_dict, n="mle"):
    df = pandas.DataFrame(in_dict).T
    uids = in_dict.keys()
    pca = PCA(n_components=n)
    matrix = df.to_numpy()
    pca.fit(matrix)
    print(pca.explained_variance_ratio_)
    matrix = pca.transform(matrix)

    df = pandas.DataFrame(matrix)
    df["uid"] = uids
    data = df.set_index("uid").T.to_dict("list")
    # print(df)
    return data

#calcuate the corrlation between the feature and the output
def get_corr(in_dict, out_dict, labels_of_input=False, heatmap=False, reduce_dim=False, corr_method='kendall'):
    if reduce_dim:
        in_dict = input_pca(in_dict)
    d = concat_dicts_by_uid(in_dict, out_dict)
    df = pandas.DataFrame(d).T
    labels = list(df)
    labels = labels[:-3]
    if labels_of_input and len(labels_of_input) == len(labels):
        labels = [i.capitalize() for i in labels_of_input]
    else:
        for i in range(0, len(labels)):
            labels[i] = "X" + str(labels[i])
    labels = labels + ["FlourishingScale", "Positive", "Negative"]

    df.columns = labels
    corr = df.corr(method=corr_method)
    corr = corr[["FlourishingScale", "Positive", "Negative"]]
    corr = corr.drop(index=["FlourishingScale", "Positive", "Negative"])
    if heatmap:
        f, ax = plt.subplots(figsize=(12, 10))
        cmaps = [plt.cm.Greens, plt.cm.Reds, plt.cm.Blues, plt.cm.Purples]
        ax.set_xticklabels(corr, rotation='horizontal')
        sns.heatmap(corr, annot=True, cmap=cmaps[random.randint(0, len(cmaps) - 1)])

        label_y = ax.get_yticklabels()
        plt.setp(label_y, rotation=360)
        label_x = ax.get_xticklabels()
        plt.setp(label_x, rotation=0)
        plt.show()
    return corr

#select features that correlation with the output larger than the input threshold
def get_corr_with_threshold(in_dict, out_dict, threshold=0.1, corr_method='pearson'):
    d = concat_dicts_by_uid(in_dict, out_dict)
    df = pandas.DataFrame(d).T
    out_labels = ["FlourishingScale", "Positive", "Negative"]
    labels = list(df)
    labels = labels[:-3]
    labels = labels + out_labels
    df.columns = labels
    corr = df.corr(method=corr_method)
    corr = corr[out_labels]
    result = {}
    for label in out_labels:
        sub_cor = corr[label]
        result[label] = []
        for i in range(len(sub_cor) - 3):
            if abs(sub_cor[i]) >= threshold:
                result[label].append(i)

    return result


if __name__ == "__main__":
    # print(fs_df)
    # print(ps_df)
    # data=get_output_value()
    # pandas.set_option('display.max_rows', data.shape[0] + 1)
    # print(data)
    activities = process_input.get_activity_data()
    # print(activities)
    print(get_corr(activities, heatmap=True, reduce_dim=True))

import process_output
import process_input
import pandas
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


def concat_dicts_by_uid(in_dict, out_dict):
    result = {}
    for uid in out_dict:
        result[uid] = in_dict[uid] + out_dict[uid]
    return result

def input_pca(in_dict,n="mle"):
    df=pandas.DataFrame(in_dict).T
    uids=in_dict.keys()
    pca=PCA(n_components=n)
    matrix=df.to_numpy()
    pca.fit(matrix)
    #print(pca.explained_variance_ratio_)
    matrix=pca.transform(matrix)

    df=pandas.DataFrame(matrix)
    df["uid"]=uids
    data=df.set_index("uid").T.to_dict("list")
    #print(df)
    return data



def get_corr(in_dict,heatmap=False,reduce_dim=False,output_type="val",corr_method='kendall'):
    if reduce_dim:
        in_dict=input_pca(in_dict)
    output = process_output.get_output_dict(output_type)
    d = concat_dicts_by_uid(in_dict, output)
    df=pandas.DataFrame(d).T
    labels=list(df)
    labels=labels[:-3]
    for i in range(0,len(labels)):
        labels[i]="X"+str(labels[i])
    labels=labels+["FlourishingScale","Positive","Negative"]

    df.columns=labels
    corr=df.corr(method=corr_method)
    corr=corr[["FlourishingScale","Positive","Negative"]]

    if heatmap:
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr, annot=True, cmap=plt.cm.Reds)
        plt.show()
    return corr

if __name__ == "__main__":
    # print(fs_df)
    # print(ps_df)
    # data=get_output_value()
    # pandas.set_option('display.max_rows', data.shape[0] + 1)
    # print(data)
    activities = process_input.get_activity_data()
    #print(activities)
    print(get_corr(activities,heatmap=True,output_type="val",reduce_dim=True))

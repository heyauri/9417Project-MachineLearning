import pandas, re
import os.path


def process_fs():
    fs_df = pandas.read_csv("StudentLife_Dataset/Outputs/FlourishingScale.csv")
    fs_df = fs_df.fillna(fs_df.mean())
    fs_df["fs"] = fs_df.sum(axis=1)
    fs_df = fs_df.groupby(fs_df['uid'])['fs'].mean().reset_index()
    return fs_df


def process_panas():
    ps_df = pandas.read_csv("StudentLife_Dataset/Outputs/panas.csv")
    pandas.set_option('display.max_rows', ps_df.shape[0] + 1)
    # Remove space in labels of columns
    # Some of the labels in pdf are not in the csv. Orz. Hence, we can not use the index directly.
    ps_df = ps_df.fillna(ps_df.mean())
    label_list = list(ps_df)
    label_list = label_list[2:]
    rn_dict = {}
    for label in label_list:
        s = re.sub(" ", "", label)
        if label != s:
            rn_dict[label] = s
    ps_df = ps_df.rename(columns=rn_dict)
    label_list = list(ps_df)
    label_list = label_list[2:]
    positive_list = ["Interested", "Excited", "Strong", "Enthusiastic", "Proud", "Alert", "Inspired", "Determined",
                     "Attentive", "Active"]
    negative_list = ["Distressed", "Upset", "Guilty", "Scared", "Hostile", "Irritable", "Ashamed", "Nervous", "Jittery",
                     "Afraid"]
    positive_list = [item for item in positive_list if item in label_list]
    negative_list = [item for item in negative_list if item in label_list]
    # generate new cols
    ps_df["positive"] = ps_df[positive_list].sum(axis=1)
    ps_df["negative"] = ps_df[negative_list].sum(axis=1)
    ps_df = ps_df.groupby(ps_df['uid'])['positive', 'negative'].mean().reset_index()
    return ps_df

#Process the output values
def get_output_value():
    fs_df = process_fs()
    ps_df = process_panas()
    data = pandas.merge(fs_df, ps_df, on='uid')
    return data


def classify_by_median(d):
    df = pandas.DataFrame(d).T
    labels = ["fs", "Positive", "Negative"]
    df.columns = labels
    arr_median = [df["fs"].median(), df["Positive"].median(), df["Negative"].median()]
    #print(df)
    for i in range(3):
        label = labels[i]
        tmp = []
        arr = df[label].to_list()
        for val in arr:
            if val > arr_median[i]:
                tmp.append(1)
            else:
                tmp.append(0)
        df[label] = tmp
    return df.T.to_dict("list")

#convert dataFrame to a dict
def get_output_dict(result_type="val"):
    csv_path = "./processed_data/output_value.csv"
    if os.path.isfile(csv_path):
        result = pandas.read_csv(csv_path).to_dict("list")
    else:
        data = get_output_value()
        result = data.set_index("uid").T.to_dict("list")
        df = pandas.DataFrame(result)
        df.to_csv(csv_path, index=0)
    if result_type == "class":
        res = classify_by_median(result)
        return res
    else:
        return result


if __name__ == "__main__":
    # print(fs_df)
    # print(ps_df)
    # data=get_output_value()
    # pandas.set_option('display.max_rows', data.shape[0] + 1)
    # print(data)
    print(get_output_dict(result_type="class"))

import pandas

fs_df=pandas.read_csv("StudentLife_Dataset/Outputs/FlourishingScale.csv")
fs_df=fs_df.fillna(fs_df.mean())
fs_df["value"]=fs_df.sum(axis=1)
fs_median=fs_df["value"].median()
print(fs_median)

ps_df=pandas.read_csv("StudentLife_Dataset/Outputs/panas.csv")
pandas.set_option('display.max_rows', ps_df.shape[0] + 1)

ps_df=ps_df.fillna(ps_df.mean())
ps_df["value"]=ps_df.sum(axis=1)
print(ps_df)
ps_df=ps_df.groupby(ps_df['uid'])['value'].sum().reset_index()
print(ps_df)
ps_median=ps_df["value"].median()
print(ps_median)

if __name__ == "__main__":
    pandas.set_option('display.max_rows', fs_df.shape[0] + 1)
    print(fs_df)
    print(ps_df)
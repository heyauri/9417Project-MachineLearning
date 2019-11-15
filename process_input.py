import os.path
from data_export import activity, audio, conversation, start_end_timestamp, bt, wifi
import glob, re
import pandas


def get_uid_from_filename(fn):
    s = str(fn)
    arr = s.split("/")
    s = arr[-1]
    s = re.sub(r"^.*_", "", s)
    s = re.sub(r"\..*", "", s)
    return s


def get_activity_data():
    csv_path = "./processed_data/activity.csv"
    if os.path.isfile(csv_path):
        return pandas.read_csv(csv_path).to_dict("list")

    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/activity/*.csv')
    res = {}
    for fn in csv_group:
        print("Processing " + fn + " ...")
        uid = get_uid_from_filename(fn)
        data = activity.process_acts(fn)
        res[uid] = data

    df = pandas.DataFrame(res)
    df.to_csv(csv_path, index=0)
    return res


def get_audios_data():
    csv_path = "./processed_data/audio.csv"
    if os.path.isfile(csv_path):
        return pandas.read_csv(csv_path).to_dict("list")

    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/audio/*.csv')
    res = {}
    for fn in csv_group:
        print("Processing " + fn + " ...")
        uid = get_uid_from_filename(fn)
        data = audio.process_audios(fn)
        res[uid] = data

    df = pandas.DataFrame(res)
    df.to_csv(csv_path, index=0)
    return res


def get_conversations_data():
    csv_path = "./processed_data/conversation.csv"
    if os.path.isfile(csv_path):
        return pandas.read_csv(csv_path).to_dict("list")

    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/conversation/*.csv')
    res = {}
    for fn in csv_group:
        print("Processing " + fn + " ...")
        uid = get_uid_from_filename(fn)
        data = conversation.process_conversations(fn)
        res[uid] = data
    df = pandas.DataFrame(res)
    df.to_csv(csv_path, index=0)
    return res


def get_phonecharge_data():
    csv_path = "./processed_data/phonecharge.csv"
    if os.path.isfile(csv_path):
        return pandas.read_csv(csv_path).to_dict("list")

    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/phonecharge/*.csv')
    res = {}
    for fn in csv_group:
        print("Processing " + fn + " ...")
        uid = get_uid_from_filename(fn)
        data = start_end_timestamp.process_start_end(fn)
        res[uid] = data
    df = pandas.DataFrame(res)
    df.to_csv(csv_path, index=0)
    return res


def get_dark_data():
    csv_path = "./processed_data/dark.csv"
    if os.path.isfile(csv_path):
        return pandas.read_csv(csv_path).to_dict("list")

    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/dark/*.csv')
    res = {}
    for fn in csv_group:
        print("Processing " + fn + " ...")
        uid = get_uid_from_filename(fn)
        data = start_end_timestamp.process_start_end(fn)
        res[uid] = data
    df = pandas.DataFrame(res)
    df.to_csv(csv_path, index=0)
    return res


def get_phonelock_data():
    csv_path = "./processed_data/phonelock.csv"
    if os.path.isfile(csv_path):
        return pandas.read_csv(csv_path).to_dict("list")

    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/phonelock/*.csv')
    res = {}
    for fn in csv_group:
        print("Processing " + fn + " ...")
        uid = get_uid_from_filename(fn)
        data = start_end_timestamp.process_start_end(fn)
        res[uid] = data
    df = pandas.DataFrame(res)
    df.to_csv(csv_path, index=0)
    return res


def get_bt_data():
    csv_path = "./processed_data/bluetooth.csv"
    if os.path.isfile(csv_path):
        return pandas.read_csv(csv_path).to_dict("list")

    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/bluetooth/*.csv')
    res = {}
    for fn in csv_group:
        print("Processing " + fn + " ...")
        uid = get_uid_from_filename(fn)
        data = bt.process_bts(fn)
        res[uid] = data
    df = pandas.DataFrame(res)
    df.to_csv(csv_path, index=0)
    return res


def get_wifi_data():
    csv_path = "./processed_data/wifi.csv"
    if os.path.isfile(csv_path):
        return pandas.read_csv(csv_path).to_dict("list")

    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/wifi/*.csv')
    res = {}
    for fn in csv_group:
        print("Processing " + fn + " ...")
        uid = get_uid_from_filename(fn)
        data = bt.process_bts(fn)
        res[uid] = data
    df = pandas.DataFrame(res)
    df.to_csv(csv_path, index=0)
    return res


if __name__ == "__main__":
    # print(fs_df)
    # print(ps_df)
    # data=get_output_value()
    # pandas.set_option('display.max_rows', data.shape[0] + 1)
    # print(data)
    # get_activity_data()

    d = {"ss": [1, 2, 3], "ssd": [2, 3, 4]}
    t = pandas.DataFrame(d)
    print(t)
    t.to_csv("t.csv", index=0)
    t = pandas.read_csv("t.csv")
    print(t)
    t = t.to_dict("list")
    print(t)

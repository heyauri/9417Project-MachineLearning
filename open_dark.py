import os
import csv
import glob
import time as t
from datetime import datetime

def call():
    # read the csv from 'dark' file folder
    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/dark/*.csv')
    for i in csv_group:
        with open(i, encoding='utf-8') as csv_files:
            reader = csv.reader(csv_files)
            i = str(i).split("_")
            i = str(i[2]).split(".")
            user_id = i[0]
            time = list(reader)
            # Traversing timestamp, changing the timestamp to time
            tmp = []
            for whole_time in time[1:]:
                res = []
                for start_end_time in whole_time:
                    time_local = t.localtime(int(start_end_time))
                    start_end_time = t.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    res.append(start_end_time)
                tmp.append(res)
            # start_end_time dictionary
            start_end_time = {}
            start_end_time[user_id] = tmp
            # this dictionary is in the form of {'u34': [['2013-03-28 12:11:51', '2013-03-28 14:36:18'], ...]}
            # print(start_end_time)

    # use timestamp to do the subtracting of timestamp
    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/dark/*.csv')
    for i in csv_group:
        with open(i, encoding='utf-8') as csv_files:
            reader = csv.reader(csv_files)
            i = str(i).split("_")
            i = str(i[2]).split(".")
            user_id = i[0]
            time = list(reader)
            # Traversing timestamp, changing the timestamp to time
            minus = []
            for whole_time in time[1:]:
                subtracting = int(whole_time[1]) - int(whole_time[0])
                minus.append(subtracting)
            # this dictionary is in the form of {'u00': [19783, 4705, 4977,...]}
            timestamp_subtracting = {}
            timestamp_subtracting[user_id] = minus

            # print(timestamp_subtracting)
            # this dictionary is in the form of {'u00': 1765650}
            sum_time = sum(minus)
            # print(sum_time)

    # use the hour of start and end time on behalf of the time
    moafevni = {}

    timestamp_subtracting = {}
    csv_group = glob.glob('./StudentLife_Dataset/Inputs/sensing/dark/*.csv')
    for i in csv_group:
        with open(i, encoding='utf-8') as csv_files:
            reader = csv.reader(csv_files)
            i = str(i).split("_")
            i = str(i[2]).split(".")
            user_id = i[0]
            time = list(reader)
            tmp = []
            for whole_time in time[1:]:

                # calculate the second of the interval of time
                subtracting = int(whole_time[1]) - int(whole_time[0])
                minus.append(subtracting)
                # this dictionary timestamp_subtracting is in the form of {'u00': [19783, 4705, 4977,...]}
                timestamp_subtracting[user_id] = [sum(minus)]
                # print(timestamp_subtracting)
                # this dictionary sum_time is in the form of {'u00': 1765650}
                sum_time = sum(minus)
                # print(sum_time)

                hour = []
                for start_end_time in whole_time:
                    time_local = t.localtime(int(start_end_time))
                    start_end_time = t.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    d = datetime.strptime(start_end_time, "%Y-%m-%d %H:%M:%S")
                    hour.append(d.hour)
                tmp.append(hour)
                # print(hour)

            # print(timestamp_subtracting)
            # 分类需要改进一下
            morning = []
            afternoon = []
            evening = []
            night = []
            # print(tmp)
            # print(len(tmp))
            for i in range(len(tmp)):
                one = tmp[i]
                # print(one)
                if one[0] >= 7 and one[0] <= 12:
                    # print(tmp.index(one))
                    morning.append(minus[i])
                elif one[0] > 12 and one[0] <= 18:
                    # print(timestamp_subtracting[i])
                    afternoon.append(minus[i])
                elif one[0] > 18 and one[0] <= 23:
                    evening.append(minus[i])
                elif one[0] >= 23 or one[0] < 7:
                    night.append(minus[i])
            # print(morning)
            # this dictionary is in the form of {'u00': [[17, 22], [23, 0], [4, 6],...]}
            dic_corresponding = {}
            dic_corresponding[user_id] = tmp
            # print(dic_hour)
            # this dictionary is in the form of {'u00': ['afternoon', 'evening', 'night', 'morning', 'night', 'morning',...]}
            # moafevni = {}
            # print(len(tmp))
            ass = []
            ass.append(sum(morning))
            ass.append(sum(afternoon))
            ass.append(sum(evening))
            ass.append(sum(night))
            moafevni[user_id] = ass
    #print(moafevni)
    # tmp is in the form of [[17, 22], [21, 50], [6, 49], [23, 0], ...]
    # print(tmp)
    #print(timestamp_subtracting)
    return timestamp_subtracting
 


























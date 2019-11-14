import os
import csv
import glob
import time as t
from datetime import datetime


# use the hour of start and end time on behalf of the time
moafevni = {}
timestamp_subtracting = {}
def process_start_end(i):
    with open(i, encoding = 'utf-8') as csv_files:
        reader = csv.reader(csv_files)
        i = str(i).split("_")
        i = str(i[2]).split(".")
        user_id = i[0]
        time = list(reader)
        minus = []
        for whole_time in time[1:]:
            subtracting = int(whole_time[1]) - int(whole_time[0])
            minus.append(subtracting)
        # this dictionary is in the form of {'u00': [19783, 4705, 4977,...]}
        timestamp_subtracting = {}
        timestamp_subtracting[user_id] = minus
        # this dictionary is in the form of {'u00': 1765650}

        tmp_1 = []
        for whole_time in time[1:]:
            res = []
            for start_end_time in whole_time:
                time_local = t.localtime(int(start_end_time))
                start_end_time = t.strftime("%Y-%m-%d %H:%M:%S",time_local)
                res.append(start_end_time)
            tmp_1.append(res)
        # start_end_time dictionary
        # this dictionary is in the form of {'u34': [['2013-03-28 12:11:51', '2013-03-28 14:36:18'], ...]}
        start_end_time = {}
        start_end_time[user_id] = tmp_1

        tmp = []
        for whole_time in time[1:]:
            # calculate the second of the interval of time
            subtracting = int(whole_time[1]) - int(whole_time[0])
            minus.append(subtracting)
            # this dictionary timestamp_subtracting is in the form of {'u00': [19783, 4705, 4977,...]}    
            timestamp_subtracting[user_id] = sum(minus)
            hour = []
            for start_end_time in whole_time:
                time_local = t.localtime(int(start_end_time))
                start_end_time = t.strftime("%Y-%m-%d %H:%M:%S",time_local)
                d = datetime.strptime(start_end_time,"%Y-%m-%d %H:%M:%S")
                hour.append(d.hour)
            tmp.append(hour)
        morning, afternoon, evening, night = [], [], [], []
        for i in range(len(tmp)):
            one=tmp[i]
            if one[0] >= 7 and one[0] <= 12:
                morning.append(minus[i])
            elif one[0] > 12 and one[0] <= 18:
                afternoon.append(minus[i])
            elif one[0] > 18 and one[0] <= 23:
                evening.append(minus[i])
            elif one[0] >= 23 or one[0] < 7:
                night.append(minus[i])
        # this dictionary is in the form of {'u00': [[17, 22], [23, 0], [4, 6],...]}
        dic_corresponding = {}
        dic_corresponding[user_id] = tmp
        # this dictionary is in the form of {'u00': ['afternoon', 'evening', 'night', 'morning', 'night', 'morning',...]}
        duration = []
        duration.append(round(sum(morning)/5788800,4))
        duration.append(round(sum(afternoon)/5788800,4))
        duration.append(round(sum(evening)/5788800,4))
        duration.append(round(sum(night)/5788800,4))
        moafevni[user_id] = duration

    return duration

 

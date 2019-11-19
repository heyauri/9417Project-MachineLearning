import csv
import numpy as np
import time
import glob
from collections import defaultdict
from datetime import datetime
import re


def process_wifi_location(fn):
    data = []
    csv_files = open(fn, encoding='utf-8')
    csv_reader = csv.reader(csv_files)
    for row in csv_reader:
        if row != []:
            data.append(row)
    data_raw = np.array(data[1:])
    # print(data_raw)
    time = data_raw[:, 0]
    location = data_raw[:, 1]

    building_time_dic = {}
    for i in location:
        if i[:2] == 'in':
            tmp = re.compile(r'[[](.*?)[]]', re.S)
            in_building = re.findall(tmp, i)
            if in_building[0] not in building_time_dic:
                building_time_dic[in_building[0]] = 1
            else:
                building_time_dic[in_building[0]] += 1
        # print(building_time_dic)
        else:
            tmp_1 = re.compile(r'[[](.*?)[]]', re.S)
            near_building = re.findall(tmp_1, i)
            near_building_split = near_building[0].strip().replace(' ', '').split(";")
            # print(near_building_split)
            # print(near_building_split)
            for j in near_building_split:
                if j != '':
                    if j in building_time_dic:
                        building_time_dic[j] += 0.5
                    if j not in building_time_dic:
                        building_time_dic[j] = 0.5
    # print(building_time_dic)
    building_time_list = []
    for value in building_time_dic.values():
        building_time_list.append(value)
    building_number = len(building_time_list)
    return [building_number,sum(building_time_list)/building_number]


'''
for i in time:
    dt_object = datetime.fromtimestamp(int(i))
    date = str(dt_object.date())
    day = dt_object.day
    #print(day)

'''
# print(time)

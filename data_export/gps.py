# ignore the last column, it same with activity
import csv
import numpy as np
import time
import glob
from collections import defaultdict


def process_gps(fn):
    data = []
    csv_files = open(fn, encoding='utf-8')
    csv_reader = csv.reader(csv_files)
    for row in csv_reader:
        if row != []:
            data.append(row)
    data_raw = np.array(data[1:])
    # print(data_raw)
    provider = data_raw[:, 1]
    network = data_raw[:, 2]
    accuracy = data_raw[:, 3]
    bearing = data_raw[:, 7]
    speed = data_raw[:, 8]

    # mining house of provider
    count_net = 0
    count_gps = 0
    # provider_list= []
    gps = []
    for i in provider:
        if i == 'network':
            count_net += 1
        if i == 'gps':
            count_gps += 1
    gps.append(count_net)
    gps.append(count_gps)
    # print(provider_list)
    # mining house of wifi
    count_wifi = 0
    count_cell = 0
    # network_list = []
    for i in network:
        if i == 'wifi':
            count_wifi += 1
        if i == 'cell':
            count_cell += 1
    # print(network_list)

    # average of accuracy
    accuracy_sum = 0
    for i in accuracy:
        accuracy_sum += float(i)
    accuracy_average = round(accuracy_sum / len(accuracy), 2)
    # print(accuracy_average)

    # average of bearing
    bearing_sum = 0
    for i in bearing:
        bearing_sum += float(i)
    bearing_average = round(bearing_sum / len(bearing), 2)
    # print(bearing_average)

    # average of speed
    speed_sum = 0
    for i in speed:
        speed_sum += float(i)
    speed_average = round(speed_sum / len(speed), 2)
    # print(speed_average)

    gps.append(count_wifi)
    gps.append(count_cell)
    gps.append(accuracy_average)
    gps.append(bearing_average)
    gps.append(speed_average)
    return gps

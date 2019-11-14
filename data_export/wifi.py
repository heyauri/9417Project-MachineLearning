import glob, csv, os
from datetime import datetime
from collections import defaultdict

def dict_slice(adict, start, end):
    keys = list(adict.keys())
    dict_slice = {}
    for k in keys[start: end]:
        dict_slice[k] = adict[k]
    return dict_slice

dir = r'C:\2019-T3\9417\StudentLife_Dataset\StudentLife_Dataset\Inputs\sensing\wifi'
file_names = list(os.walk(dir))[0][2]
uid = []

csvfile = open('wifi/wifi_u00.csv')
csvreader = csv.reader(csvfile)
bssid, freq = {}, {}
for row in csvreader:
    if row and 'time' not in row:
        if row[1] not in bssid:
            bssid[row[1]] = [1, row[3]]#bssid = {BSSID: c, level}
        else:
            bssid[row[1]][0] += 1
            bssid[row[1]].append(row[3])
        if row[2] not in freq:
            freq[row[2]] = 1#freq = {freq: c}
        else:
            freq[row[2]] += 1
#print(bssid)

bssids = {}
for k, v in bssid.items():
    mean = sum(int(e) for e in v[1:]) / (len(v) - 1)
    #bssid[k] = [v[0], round(mean, 3)]
    if mean != 0.0:
        bssids[k] = [v[0] * round(mean, 3)]
#print(bssids['00:22:6b:84:66:26'])


t = sum(freq[k] for k in freq.keys())
for k, v in freq.items():
    por = round((freq[k] / t) * 100, 3)
    freq[k] = por
#print(freq)

bssids = dict(sorted(bssids.items(), key = lambda x: x[1], reverse = True))
bssids_slice = dict_slice(bssids, 0, 20)
print(bssids_slice)

freq = dict(sorted(freq.items(), key = lambda x: x[1], reverse = True))
freq_slice = dict_slice(freq, 0, 20)
#print(freq_slice)

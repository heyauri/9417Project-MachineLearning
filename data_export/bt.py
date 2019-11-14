import glob, csv, os
from datetime import datetime
from collections import defaultdict

def dict_slice(adict, start, end):
    keys = list(adict.keys())
    dict_slice = {}
    for k in keys[start: end]:
        dict_slice[k] = adict[k]
    return dict_slice

dir = r'C:\2019-T3\9417\StudentLife_Dataset\StudentLife_Dataset\Inputs\sensing\bluetooth'
file_names = list(os.walk(dir))[0][2]
uid = []
'''
for i in range(len(file_names)):
    ID = file_names[i].split('_')[1][0: 3]
    uid.append(ID)
    csvfile = open('bluetooth/' + f'{file_names[i]}')
    csvreader = csv.reader(csvfile)

    site, classid = {}, {}
    for row in csvreader:
        if row and 'time' not in row:
            if row[1] not in site:
                site[row[1]] = [1, row[3]]#site = {MAC: c, level}
            else:
                site[row[1]][0] += 1
                site[row[1]].append(row[3])
            if row[2] not in classid:
                classid[row[2]] = 1
            else:
                classid[row[2]] += 1
'''
csvfile = open('bluetooth/bt_u00.csv')
csvreader = csv.reader(csvfile)
site, classid = {}, {}
for row in csvreader:
    if row and 'time' not in row:
        if row[1] not in site:
            site[row[1]] = [1, row[3]]#site = {MAC: c, level}
        else:
            site[row[1]][0] += 1
            site[row[1]].append(row[3])
        if row[2] not in classid:
            classid[row[2]] = 1#classid = {classid: c}
        else:
            classid[row[2]] += 1

sites = {}
for k, v in site.items():
    mean = sum(int(e) for e in v[1:]) / (len(v) - 1)
    #sites[k] = [v[0], round(mean, 3)]
    if mean != 0.0:
        sites[k] = [v[0] * round(mean, 3)]

t = sum(classid[k] for k in classid.keys())
for k, v in classid.items():
    por = round((classid[k] / t) * 100, 3)
    classid[k] = por
#print(classid)

sites = dict(sorted(sites.items(), key = lambda x: x[1][0], reverse = True))
sites_slice = dict_slice(sites, 0, 20)
print(sites_slice)

classid = dict(sorted(classid.items(), key = lambda x: x[1], reverse = True))
class_slice = dict_slice(classid, 0, 20)
#print(class_slice)
    


















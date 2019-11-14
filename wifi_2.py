import glob, csv, os
from datetime import datetime
from collections import defaultdict

def deal_wifi(csvreader):
    bssid, freq = {}, {}
    level = [None] * 3
    c1, c2, c3 = 0, 0, 0
    for row in csvreader:
        if row and 'time' not in row:
            if row[1] not in bssid:
                bssid[row[1]] = [1]#bssid = {MAC: c}
            else:
                bssid[row[1]][0] += 1
            if row[2] not in freq:
                freq[row[2]] = [1]#classid = {freq: c, level}
            else:
                freq[row[2]][0] += 1
            if -70 < int(row[3])  <= 0:
                c1 += 1
                level[0] = c1
            elif -80 < int(row[3]) <= -70:
                c2 += 1
                level[1] = c2
            else:
                c3 += 1
                level[2] = c3

    r = []
    tbssid = sum(v[0] for k, v in bssid.items())
    mbssid = round(tbssid / len(bssid), 3)
    r.append(mbssid)

    tfreq = sum(v[0] for k, v in freq.items())
    mfreq = round(tfreq / len(freq), 3)
    r.append(mfreq)

    m1 = round(100 * (level[0] / sum(level)), 3)
    m2 = round(100 * (level[1] / sum(level)), 3)
    m3 = round(100 * (level[2] / sum(level)), 3)
    r.append(m1)
    r.append(m2)
    r.append(m3)
    
    return r


def get_wifi():
    dir = './StudentLife_Dataset/Inputs/sensing/wifi/'
    file_names = list(os.walk(dir))[0][2]#'activity_u00.csv', 'activity_u01.csv'...
    uid, result = [], defaultdict(list)

    for i in range(len(file_names)):
        ID = file_names[i].split('_')[1][0: 3]
        uid.append(ID)
        csvfile = open(dir + f'{file_names[i]}')
        csvreader = csv.reader(csvfile)
        result[uid[i]] = deal_wifi(csvreader)

    return result

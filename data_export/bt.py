import glob, csv, os
from datetime import datetime
from collections import defaultdict

def process_bts(fn):
    with open(fn) as csvfile:
        csvreader = csv.reader(csvfile)
        site, classid = {}, {}
        level = [None] * 3
        c1, c2, c3 = 0, 0, 0
        for row in csvreader:
            if row and 'time' not in row:
                if row[1] not in site:
                    site[row[1]] = [1]#site = {MAC: c}
                else:
                    site[row[1]][0] += 1
                if row[2] not in classid:
                    classid[row[2]] = [1]#classid = {classid: c, level}
                else:
                    classid[row[2]][0] += 1
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
        tsite = sum(v[0] for k, v in site.items())
        msite = round(tsite / len(site), 3)
        r.append(msite)

        tclass = sum(v[0] for k, v in classid.items())
        mclass = round(tclass / len(classid), 3)
        r.append(mclass)

        m1 = round(100 * (level[0] / sum(level)), 3)
        m2 = round(100 * (level[1] / sum(level)), 3)
        m3 = round(100 * (level[2] / sum(level)), 3)
        r.append(m1)
        r.append(m2)
        r.append(m3)

        return r


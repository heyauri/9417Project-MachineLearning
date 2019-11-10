from datetime import datetime
import csv

dt_object = datetime.fromtimestamp(1364356801)

print(dt_object.date())

dict_days_total = {}
dict_days_by_period = {}
default = {0: 0, 1: 0, 2: 0, 3: 0}

fn = "../StudentLife_Dataset/Inputs/sensing/activity/activity_u00.csv"


def cal_daily_data(total,by_period):
    # total
    arr_total={0: [], 1: [], 2: [], 3: []}
    for date in total:
        total_acts=sum(total[date].values())
        for key in total[date]:
            arr_total[key].append(total[date][key]/total_acts)
    for key in arr_total:
        arr_total[key]=sum(arr_total[key])/len(arr_total[key])

    return arr_total

def process_acts(fn):
    with open(fn) as f:
        acts = csv.reader(f)
        for line in acts:
            if len(line) < 1 or line[0] == "timestamp":
                continue
            dt_object = datetime.fromtimestamp(int(line[0]))
            date = str(dt_object.date())

            ## count activities per day
            if date not in dict_days_total:
                dict_days_total[date] = default.copy()
            for key in range(4):
                if key == int(line[1]):
                    dict_days_total[date][key] += 1
            ## count activities per day and devided into each period
            if date not in dict_days_by_period:
                dict_days_by_period[date] = {
                    "morning": default.copy(), "noon": default.copy(),
                    "evening": default.copy(), "night": default.copy()
                }
            for key in range(4):
                if key == int(line[1]):
                    hour = dt_object.hour
                    if hour < 5 or hour >= 20:
                        dict_days_by_period[date]["night"][key] += 1
                    elif 5 <= hour < 11:
                        dict_days_by_period[date]["morning"][key] += 1
                    elif 11 <= hour < 17:
                        dict_days_by_period[date]["noon"][key] += 1
                    elif 17 <= hour < 20:
                        dict_days_by_period[date]["evening"][key] += 1

        data=cal_daily_data(dict_days_total,dict_days_by_period)
        print(data)




if __name__ == "__main__":
    process_acts(fn)

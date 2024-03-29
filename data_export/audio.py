from datetime import datetime
import csv
import glob

dict_days_total = {}
dict_days_by_period = {}
default = {0: 0, 1: 0, 2: 0}

fn = "../StudentLife_Dataset/Inputs/sensing/audio/audio_u00.csv"


def cal_daily_data(total, by_period):
    # total
    arr_total = {0: [], 1: [], 2: []}
    average_total = {0: [], 1: [], 2: []}
    for date in total:
        total_acts = sum(total[date].values())
        for key in total[date]:
            arr_total[key].append(total[date][key])
            average_total[key].append(total[date][key] / total_acts)
    # period
    arr_period = {}
    average_period = {}
    for date in by_period:
        for period in by_period[date]:
            if period not in arr_period:
                arr_period[period] = {0: [], 1: [], 2: []}
                average_period[period] = {0: [], 1: [], 2: []}
            period_acts = sum(by_period[date][period].values())
            if period_acts < 1:
                continue
            for key in range(3):
                arr_period[period][key].append(by_period[date][period][key])
                average_period[period][key].append(by_period[date][period][key] / period_acts)
    # calculate mean of daily value
    result = []
    temp_total={}

    for key in arr_total:
        temp_total[key] = sum(arr_total[key]) / len(arr_total[key])
        average_total[key] = sum(average_total[key]) / len(average_total[key])
        result.append(sum(arr_total[key]))
        result.append(temp_total[key])
        result.append(average_total[key])
    for period in arr_period:
        for key in range(3):
            if len(arr_period[period][key]):
                arr_period[period][key] = sum(arr_period[period][key]) / len(arr_period[period][key])
                average_period[period][key] = sum(average_period[period][key]) / len(average_period[period][key])
            else:
                arr_period[period][key] = 0
                average_period[period][key] = 0
            result.append(arr_period[period][key])
            result.append(average_period[period][key])
    return result


def process_audios(fn):
    with open(fn) as f:
        acts = csv.reader(f)
        for line in acts:
            if len(line) < 1 or line[0] == "timestamp":
                continue
            dt_object = datetime.fromtimestamp(int(line[0]))
            date = str(dt_object.date())

            ## count audios per day
            if date not in dict_days_total:
                dict_days_total[date] = default.copy()
            for key in range(3):
                if key == int(line[1]):
                    dict_days_total[date][key] += 1
            ## count audios per day and devided into each period
            if date not in dict_days_by_period:
                dict_days_by_period[date] = {
                    "day": default.copy(), "night": default.copy()
                }
            for key in range(3):
                if key == int(line[1]):
                    hour = dt_object.hour
                    if hour < 6 or hour >= 20:
                        dict_days_by_period[date]["night"][key] += 1
                    else:
                        dict_days_by_period[date]["day"][key] += 1

        data = cal_daily_data(dict_days_total, dict_days_by_period)
        # print(dict_days_total)
        # print(dict_days_by_period)
        return data


if __name__ == "__main__":
    print(process_audios(fn))

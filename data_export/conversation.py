from datetime import datetime
import csv
import glob

dict_days_total = {}
dict_days_by_period = {}
duration_days_total = {}
duration_days_by_period = {}

fn = "../StudentLife_Dataset/Inputs/sensing/conversation/conversation_u00.csv"


def cal_daily_data(total, by_period,duration_dict, duration_by_period):
    timestamp_subtracting = {} # total
    arr_total = {0: [], 1: [], 2: []}
    for date in total:
        total_acts = sum(total[date].values())
        for key in total[date]:
            arr_total[key].append(total[date][key] / total_acts)
    # period
    arr_period = {}
    for date in by_period:
        for period in by_period[date]:
            if period not in arr_period:
                arr_period[period] = {0: [], 1: [], 2: []}
            period_acts = sum(by_period[date][period].values())
            if period_acts < 1:
                continue
            for key in range(3):
                arr_period[period][key].append(by_period[date][period][key] / period_acts)
    # calculate mean of daily value
    result = []
    for key in arr_total:
        arr_total[key] = sum(arr_total[key]) / len(arr_total[key])
        result.append(arr_total[key])
    for period in arr_period:
        for key in range(3):
            arr_period[period][key] = sum(arr_period[period][key]) / len(arr_period[period][key])
            result.append(arr_period[period][key])
    return result


def process_conversations(fn):
    with open(fn) as f:
        conversations = csv.reader(f)
        for line in conversations:
            if len(line) < 1 or line[0] == "start_timestamp":
                continue
            start_time_obj = datetime.fromtimestamp(int(line[0]))
            end_time_obj = datetime.fromtimestamp(int(line[1]))
            duration = int(line[1]) - int(line[0])
            date = str(start_time_obj.date())

            ## count conversation frequency per day
            if date not in dict_days_total:
                dict_days_total[date] = 1
                duration_days_total[date] = duration
            else:
                dict_days_total[date] += 1
                duration_days_total[date] += duration

            ## count conversations per day and devided into each period
            if date not in dict_days_by_period:
                dict_days_by_period[date] = {
                    "day": 0, "night": 0
                }
            if date not in duration_days_by_period:
                duration_days_by_period[date] = {
                    "day": 0, "night": 0
                }
            hour = start_time_obj.hour
            if hour < 5 or hour >= 20:
                dict_days_by_period[date]["night"] += 1
                duration_days_by_period[date]["night"] += duration
            else:
                dict_days_by_period[date]["day"] += 1
                duration_days_by_period[date]["day"] += duration

        data = cal_daily_data(dict_days_total, dict_days_by_period,duration_days_total,duration_days_by_period)
        # print(dict_days_total)
        # print(dict_days_by_period)
        return data


if __name__ == "__main__":
    print(process_conversations(fn))

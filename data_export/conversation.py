from datetime import datetime
import csv
import glob

dict_days_total = {}
dict_days_by_period = {}
duration_days_total = {}
duration_days_by_period = {}
long_time_freq = {}
long_time_duration = {}

fn = "../StudentLife_Dataset/Inputs/sensing/conversation/conversation_u00.csv"


def cal_daily_data(total, by_period, duration_dict, duration_by_period):
    result = []
    # total
    freq_total = total.values()
    result.append(sum(freq_total) / len(freq_total))
    duration_total = duration_dict.values()
    result.append(sum(duration_total) / len(duration_total))
    # average conversation duration
    result.append(result[1] / result[0])
    # long time conversation
    freq_long_time = long_time_freq.values()
    duration_long_time = long_time_duration.values()
    result.append(sum(freq_long_time) / len(freq_long_time))
    result.append(sum(duration_long_time) / len(duration_long_time))
    result.append(result[-1] / result[-2])
    # period
    freq_period = {}
    duration_period = {}
    average_duration_period = {}
    for date in by_period:
        for period in by_period[date]:
            if period not in freq_period:
                freq_period[period] = []
                duration_period[period] = []
                average_duration_period[period] = []
            freq = by_period[date][period]
            duration = duration_by_period[date][period]
            if not freq:
                continue
            average = duration / freq
            freq_period[period].append(freq)
            duration_period[period].append(duration)
            average_duration_period[period].append(average)
    for period in freq_period.keys():
        result.append(sum(freq_period[period]) / len(freq_period[period]))
        result.append(sum(duration_period[period]) / len(duration_period[period]))
        result.append(sum(average_duration_period[period]) / len(average_duration_period[period]))

    return result


def process_conversations(fn):
    with open(fn) as f:
        conversations = list(csv.reader(f))
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
                long_time_freq[date] = 0
                long_time_duration[date] = 0
                duration_days_total[date] = duration
            else:
                dict_days_total[date] += 1
                duration_days_total[date] += duration
            if duration > 600:
                long_time_freq[date] += 1
                long_time_duration[date] += duration

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
            if hour < 7 or hour >= 22:
                dict_days_by_period[date]["night"] += 1
                duration_days_by_period[date]["night"] += duration
            else:
                dict_days_by_period[date]["day"] += 1
                duration_days_by_period[date]["day"] += duration

        data = cal_daily_data(dict_days_total, dict_days_by_period, duration_days_total, duration_days_by_period)
        # print(dict_days_total)
        # print(dict_days_by_period)
        return data


if __name__ == "__main__":
    print(process_conversations(fn))

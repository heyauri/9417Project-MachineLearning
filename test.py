import process_input,process_output
import calc_corr




if __name__ == "__main__":
    out_dict=process_output.get_output_dict("val")

    label_dict = {
        "phonelock": ["phonelock duration during morning", "phonelock duration during afternoon",
                      "phonelock duration during evening",
                      "phonelock duration during night"],
        "phonecharge": ["phonecharge duration during morning", "phonecharge duration during afternoon",
                        "phonecharge duration during evening",
                        "phonecharge duration during night"],
        "dark": ["light duration during morning", "light duration during afternoon", "light duration during evening",
                 "light duration during night"],
        "gps": ["network times of gps provider", "gps times of gps provider", "wifi times of gps_network_type",
                "cell times of gps_network_type", "average accuracy", "average bearing", "average speed"
                ],
        "wifi_location": ["the frequency of changing building", "average duration of staying in same building"],
        "bluetooth": ["total counts of bluetooth mac address", "bluetooth class", "high strength of bluetooth level",
                      "medium strength of bluetooth level", "low strength of bluetooth level"],
        "wifi": ["total counts of wifi-bssid address", "frequency of wifi", "high strength of wifi level",
                 "medium strength of wifi level", "low strength of wifi level"],
        "activity": ["activity_0 count", "daily average activity_0 count", "daily average activity_0 ratio",
                     "activity_1 count", "daily average activity_1 count", "daily average activity_1 ratio",
                     "activity_2 count", "daily average activity_2 count", "daily average activity_2 ratio",
                     "activity_3 count", "daily average activity_3 count",
                     "daily average activity_3 ratio",
                     "daily average activity_0 count during day", "daily average activity_0 ratio during day",
                     "daily average activity_1 count during day", "daily average activity_1 ratio during day",
                     "daily average activity_2 count during day", "daily average activity_2 ratio during day",
                     "daily average activity_3 count during day", "daily average activity_3 ratio during day",
                     "daily average activity_0 count during night", "daily average activity_0 ratio during night",
                     "daily average activity_1 count during night", "daily average activity_1 ratio during night",
                     "daily average activity_2 count during night", "daily average activity_2 ratio during night",
                     "daily average activity_3 count during night",
                     "daily average activity_3 ratio during night",
                     ],
        "audio": ["audio_0 count", "daily average audio_0 count", "daily average audio_0 ratio",
                  "audio_1 count", "daily average audio_1 count", "daily average audio_1 ratio",
                  "audio_2 count", "daily average audio_2 count", "daily average audio_2 ratio",
                  "daily average audio_0 count during day", "daily average audio_0 ratio during day",
                  "daily average audio_1 count during day", "daily average audio_1 ratio during day",
                  "daily average audio_2 count during day", "daily average audio_2 ratio during day",
                  "daily average audio_0 count during night", "daily average audio_0 ratio during night",
                  "daily average audio_1 count during night", "daily average audio_1 ratio during night",
                  "daily average audio_2 count during night", "daily average audio_2 ratio during night",
                  ],
        "conversation": ["daily frequency of conversation", "daily average conversation duration",
                         "average duration of each conversation", "daily frequency of long-time conversation(>10 mins)",
                         "daily average long-time conversation duration(>10 mins)",
                         "average duration of each long-time conversation(>10 mins)",
                         "daily frequency of conversation during day",
                         "daily average conversation duration during day",
                         "average duration of each conversation during day",
                         "daily frequency of conversation during night",
                         "daily average conversation duration during night",
                         "average duration of each conversation during night",
                         ],
    }

    in_dict = process_input.get_wifi_data()
    # in_dict= open_dark.call()
    # dict1=bt_2.get_bt()
    # dict2=wifi_2.get_wifi()
    print(calc_corr.get_corr(in_dict,out_dict, labels_of_input=label_dict["wifi"], heatmap=True,
                             reduce_dim=False, corr_method="pearson"))
    # print(calc_corr.get_corr(dict2,labels_of_input=labels_of_dark,heatmap=True,output_type="val",
    #                        reduce_dim=False,corr_method="pearson"))

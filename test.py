import process_input,process_output
import calc_corr

if __name__ == "__main__":
    out_dict=process_output.get_output_dict("val")
    # actvity
    labels_of_activities = ["daily 0 percentage", "daily 1 percentage", "daily 2 percentage", "daily 3 percentage",
                            "daily 0 during morning", "daily 1 during morning", "daily 2 during morning",
                            "daily 3 during morning",
                            "daily 0 during noon", "daily 1 during noon", "daily 2 during noon", "daily 3 during noon",
                            "daily 0 during evening", "daily 1 during evening", "daily 2 during evening",
                            "daily 3 during evening",
                            "daily 0 during night", "daily 1 during night", "daily 2 during night",
                            "daily 3 during night",
                            ]
    # audio
    labels_of_audios = ["daily 0 percentage", "daily 1 percentage", "daily 2 percentage",
                        "daily 0 during morning", "daily 1 during morning", "daily 2 during morning",
                        "daily 0 during noon", "daily 1 during noon", "daily 2 during noon",
                        "daily 0 during evening", "daily 1 during evening", "daily 2 during evening",
                        "daily 0 during night", "daily 1 during night", "daily 2 during night",
                        ]
    labels_of_dark = ["light duration in morning", "light duration in afternoon", "light duration in evening",
                      "light duration in night"]
    in_dict = process_input.get_audios_data()
    # in_dict= open_dark.call()
    # dict1=bt_2.get_bt()
    # dict2=wifi_2.get_wifi()
    print(calc_corr.get_corr(in_dict,out_dict, labels_of_input=labels_of_dark, heatmap=True,
                             reduce_dim=False, corr_method="pearson"))
    # print(calc_corr.get_corr(dict2,labels_of_input=labels_of_dark,heatmap=True,output_type="val",
    #                        reduce_dim=False,corr_method="pearson"))

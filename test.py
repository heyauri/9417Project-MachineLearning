import process_input
import calc_corr
import open_dark

if __name__ == "__main__":
    in_dict = process_input.get_activity_data()
    #actvity
    labels_of_activities=["daily 0 percentage","daily 1 percentage","daily 2 percentage","daily 3 percentage",
                     "daily 0 during morning", "daily 1 during morning", "daily 2 during morning", "daily 3 during morning",
                     "daily 0 during noon", "daily 1 during noon", "daily 2 during noon", "daily 3 during noon",
                     "daily 0 during evening", "daily 1 during evening", "daily 2 during evening", "daily 3 during evening",
                     "daily 0 during night", "daily 1 during night", "daily 2 during night", "daily 3 during night",
                     ]
    #audio
    labels_of_audios=["daily 0 percentage","daily 1 percentage","daily 2 percentage",
                     "daily 0 during morning", "daily 1 during morning", "daily 2 during morning",
                     "daily 0 during noon", "daily 1 during noon", "daily 2 during noon",
                     "daily 0 during evening", "daily 1 during evening", "daily 2 during evening",
                     "daily 0 during night", "daily 1 during night", "daily 2 during night",
                     ]
    #in_dict=process_input.get_audios_data()
    in_dict= open_dark.call()
    print(in_dict)
    print(calc_corr.get_corr(in_dict,labels_of_input=labels_of_audios,heatmap=True,output_type="class",
                             reduce_dim=False,corr_method="pearson"))

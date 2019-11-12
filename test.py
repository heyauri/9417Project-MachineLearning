import glob, re
import process_output
import process_input
import calc_corr


if __name__ == "__main__":
    in_dict = process_input.get_activity_data()
    labels_of_input=["daily 0 percentage","daily 1 percentage","daily 2 percentage","daily 3 percentage",
                     "daily 0 at morning", "daily 1 at morning", "daily 2 at morning", "daily 3 at morning",
                     "daily 0 at noon", "daily 1 at noon", "daily 2 at noon", "daily 3 at noon",
                     "daily 0 at evening", "daily 1 at evening", "daily 2 at evening", "daily 3 at evening",
                     "daily 0 at night", "daily 1 at night", "daily 2 at night", "daily 3 at night",
                     ]
    print(calc_corr.get_corr(in_dict,labels_of_input=labels_of_input,heatmap=True,output_type="val",reduce_dim=False))

import glob, re
import process_output
import process_input
import calc_corr


if __name__ == "__main__":
    in_dict = process_input.get_activity_data()

    print(calc_corr.get_corr(in_dict,heatmap=True,output_type="val",reduce_dim=False))

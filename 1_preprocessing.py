import pandas as pd
import os
import glob
import re
import matplotlib.pyplot as plt
import numpy as np
import pavlovian_functions as pv

path_to_files = r"C:\Users\mds8301\Desktop\test_2_color\Day_2"  # path where guppy output files for day are
day = re.search(r"Day_\d\d?", path_to_files)[0]

# new directory for where time stamps will be saved
extracted_ts_path = (path_to_files + f"\\{day}_extracted_timestamps")
aligned_ts_path = (path_to_files + f"\\{day}_aligned_events")
analyzed_behavior_path = (path_to_files + f"\\{day}_analyzed_behavior")

new_folders = [extracted_ts_path, aligned_ts_path, analyzed_behavior_path]

for f in new_folders:
    if not os.path.exists(f):
        os.mkdir(f)
        print("Directories created")
    else:
        print("Directory already exists")

#  search path_to_files for all directories, then find subdirs that contain 'output' - append paths to list mouse_dirs
mouse_dirs = glob.glob(path_to_files + "\**\*output_*")
event_ts = ["cue", "reward", "lick", "encoder"]
suffix = "_RDALHA.hdf5"
event_ts_suf = [i + suffix for i in event_ts]

for mouse in mouse_dirs:
    #  for each mouse output we will retrieve the file path for each event
    events = [pv.find_ts_file_path(mouse, event) for event in event_ts_suf]

    # create a dictionary where each event name is paired with the timestamp array
    event_dict = {}
    for event in events:
        event_id = os.path.basename(event).split("_")[0]
        event_ts_arr = pv.read_timestamps(event)
        event_dict[event_id] = event_ts_arr
        if len(event_dict.keys()) != len(event_ts):
            pass
        else:
            # covert dict to df, pull mouse ID from path name and save as csv in extracted timestamps folder
            df_raw_ts = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in event_dict.items()]))
            df_align_licks_to_cue = pv.align_events(df_raw_ts, "cue", "lick")
            df_align_encoder_to_cue = pv.align_events(df_raw_ts, "cue", "encoder")

            mouse_id = os.path.basename(mouse).split("-")[0]
            df_raw_ts.to_csv(f"{extracted_ts_path}\\{mouse_id}_{day}_timestamps.csv", index=False)
            df_align_licks_to_cue.to_csv(f"{aligned_ts_path}\\{mouse_id}_{day}_cue_aligned_lick_timestamps.csv",
                                         index=False)
            df_align_encoder_to_cue.to_csv(f"{aligned_ts_path}\\{mouse_id}_{day}_cue_aligned_encoder_timestamps.csv",
                                           index=False)

print("timestamps extracted analyzed and saved")

# group timestamps files by event
aligned_ts_files = pv.list_subdirs(aligned_ts_path)
lick_files = []
encoder_files = []
for f in aligned_ts_files:
    if re.search('lick', f):
        lick_files.append(f)
    elif re.search('encoder', f):
        encoder_files.append(f)
    else:
        pass

#function to calculate mean frequency of event and covnert to dataframe
def group_freq_df(event_name: str, filepath_list):
    freq_dict = {}
    for f in filepath_list:
        mouse_id = os.path.basename(f).split("_")[0]
        freq_arr = pv.calc_frequency(f)
        freq_dict[mouse_id] = freq_arr
        group_df = pd.DataFrame.from_dict(freq_dict).rolling(window=5, center=True).mean()

        group_df = (group_df.assign(
            mean=group_df.mean(axis=1),  # add mean,
            std=group_df.std(axis=1),  #  add standard deviation,
            sem=group_df.sem(axis=1),# add sem
            time_sec=np.arange(-10, 21, 0.2)) # add time column
        )
        return event_name, group_df


licks_analyzed = group_freq_df('licks',lick_files)
encoder_analyzed  = group_freq_df('enconder', encoder_files)
all_analysis=[licks_analyzed, encoder_analyzed]

for i in all_analysis:
    i[1].to_csv(f"{analyzed_behavior_path}\\{day}_group_{i[0]}_analysis.csv",
                                         index=False)
print('behavior analyzed')
#%%



import pandas as pd
import os
import glob
import re
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
            df_align_licks_to_cue.to_csv(f"{aligned_ts_path}\\{mouse_id}_{day}_cue_aligned_lick_timestamps.csv", index=False)
            df_align_encoder_to_cue.to_csv(f"{aligned_ts_path}\\{mouse_id}_{day}_cue_aligned_encoder_timestamps.csv", index=False)


print("timestamps extracted analyzed and saved")

# %%

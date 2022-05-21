import numpy as np
import pandas as pd
import h5py
import os
import glob
import functions

test = test_function("hello")
print(test)
#%%


path_to_files = r"C:\Users\mds8301\Desktop\test_2_color\Day_2"
new_folder_suffix ="_extracted_timestamps"
timestamps_path = ( path_to_files + "\\"
                    + path_to_files.split("\\")[-1] +
                    new_folder_suffix)

if not os.path.exists(timestamps_path):
    os.mkdir(timestamps_path)
    print("Directory created")
else:
    print("Directory already exists")


#  search path_to_files for all directories, then find subdirs that contain 'output' - append paths to list mouse_dirs
mouse_dirs = glob.glob(path_to_files +"\**\*output_*")
#%%

event_ts=["cue", "reward", "lick", "encoder"]
suffix = "_RDALHA"
event_ts_suf= [i+suffix for i in event_ts]
# path = mouse_dirs[0]
def get_event_timestamps(path, event):
        event_file = f"{path}\\{event}.hdf5"
        ts_arr = h5py.File(event_file, "r").get('ts')
        return np.array(ts_arr)


# print("all timestamp csv files saved")


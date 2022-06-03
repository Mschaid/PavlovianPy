# %%
import h5py
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec  # for subplots
import seaborn as sns
import pavlovian_functions as pv

# path where guppy output files for day  are
path_to_files = r"R:\Mike\LHA_dopamine\LH_NAC_Headfix_FP\Photometry\Pav Training\2_color_pav\Sucrose_to_sucralose\Training\Day_6"

day = re.search(r"Day_\d\d?", path_to_files)[0]

# new directory for where time stamps will be saved
extracted_ts_path = (path_to_files + f"\\{day}_extracted_timestamps")
aligned_ts_path = (path_to_files + f"\\{day}_aligned_events")
analyzed_behavior_path = (path_to_files + f"\\{day}_analyzed_behavior")
tidy_analysis = (path_to_files + f"\\{day}_tidy_analysis")

# list of new dirs to create
new_folders = [extracted_ts_path, aligned_ts_path,
               analyzed_behavior_path, tidy_analysis]
# create new dirs (new_folders)  in path to files
for f in new_folders:
    if not os.path.exists(f):
        os.mkdir(f)
        # print("Directories created")
    else:
        print("Directory already exists")
# %%
mouse_dirs = glob.glob(path_to_files + "\**\*output_*")
event_ts = ["Cuet", "Rwrp", "Lick", "endr"]
suffix = ".hdf5"
event_ts_suf = [i + suffix for i in event_ts]

for mouse in mouse_dirs:
    #  for each mouse output we will retrieve the file path for each event
    events = [pv.find_file_path(mouse, event) for event in event_ts_suf]

# %%


class Mouse:
    def __init__(self, path):
        self.path = path
        self.id = path.split("\\")[-1].split("-")[0]
        # self.fp_data_path=
        # self.fp_data = fp_data


mouse1 = Mouse(mouse_dirs[0])
print(mouse1.id)
mouse1.path  # %%

# %%

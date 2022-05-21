import numpy as np
import pandas as pd
import h5py
import os
import glob


path_to_files = r"R:\Mike\LHA_dopamine\LH_NAC_Headfix_FP\Photometry\Pav Training\cohort2\sucrose_training\day5"
timestamps_path = (
    path_to_files + "\\" + path_to_files.split("\\")[-1] + "_csv_timestamps"
)
if not os.path.exists(timestamps_path):
    os.mkdir(timestamps_path)
    print("Directory created")
else:
    print("Directory already exists")
#  search path_to_files for all directories, then find subdirs that contain 'output' - append paths to list mouse_dirs
mouse_dirs = []
directories = os.listdir(path_to_files)
for dir in directories:
    path = os.path.join(path_to_files, dir, dir + "_output_*")
    output_path = glob.glob(path)
    mouse_dirs.append(output_path)

mouse_dirs = [
    element for element in mouse_dirs if element != []
]  ## drop empty elements from list

#  function to extract cue and lick timestamps
def get_timestamps(dir_path):
    path = "".join(
        [str(item) for item in dir_path]
    )  # covert list index of path to pure string
    cue_file = glob.glob(str()
        path + "/**/CCue.hdf5", recursive=True
    )  #  search all directories for 'CCue.hdf5" file
    cue_file = "".join(
        [str(item) for item in cue_file]
    )  # covert list index into pure string for 'CCue.hdf5" file
    cue_h5 = h5py.File(cue_file, "r").get(
        "timestamps"
    )  # read timestamps from  'CCue.hdf5" file
    lick_file = glob.glob(
        path + "/**/Lick.hdf5", recursive=True
    )  #  search all directories for 'Lick.hdf5" file
    lick_file = "".join(
        [str(item) for item in lick_file]
    )  # covert list index into pure string for 'Lick.hdf5" file
    lick_h5 = h5py.File(lick_file, "r").get(
        "timestamps"
    )  # read timestamps from  'Lick.hdf5" file
    d = dict(
        cue=np.array(cue_h5),  # make dictioniary from cue and lick timestamps
        lick=np.array(lick_h5),
    )
    df = pd.DataFrame(
        dict([(k, pd.Series(v)) for k, v in d.items()])
    )  # covert dict into dataframe
    day = path.split("\\")[-3]  # get day ID from path
    mouse_id = path.split("\\")[-1].split("_")[0]  # get mouse ID from path
    df.to_csv(
        timestamps_path + "\\" + mouse_id + "_" + day + "_timestamps.csv"
    )  # save dataframe to csv in new_path
    print(mouse_id + " " + day + " " + "timestamps csv file saved")


for d in mouse_dirs:  # apply function all directories in mouse_dirs
    get_timestamps(d)

print("all timestamp csv files saved")

#%%

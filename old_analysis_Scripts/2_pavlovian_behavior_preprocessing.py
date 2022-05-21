# %%
import numpy as np
import pandas as pd
import os

# set path to files to read, and create new folder to save aligned trials
path_to_files = r"R:\Mike\LHA_dopamine\LH_NAC_Headfix_FP\Photometry\Pav Training\cohort2\sucrose_training\day5\day5_csv_timestamps"  #  path where raw timestamp csvs are stored
path_to_aligned_events = (
    path_to_files + "_aligned_events"
)  # creates folder where aligned trials for individual mice will be stored
path_to_analyzed_data = (
    path_to_files + "_analyzed_behavior_data"
)  # creates folder where analyzed data and plots will be stored
day_name = os.path.basename(path_to_aligned_events).split("_")[0]
if not os.path.exists(path_to_aligned_events):
    os.mkdir(path_to_aligned_events)
    print("path_to_aligned_events created")
else:
    print("path_to_aligned_events already exists")

if not os.path.exists(path_to_analyzed_data):
    os.mkdir(path_to_analyzed_data)
    print("path_to_analyzed_data created")
else:
    print("path_to_analyzed_data already exists")
# function reads data from csvs in filepath, pulls cue and lick timestamps and aligns licks for each cue to zero, then saves as new csv file in output path
def align_trials(filepath, path_to_aligned_events):  #
    # import data from csv, create array for cue and events as well as remove unwanted 0's and NaN
    data = pd.read_csv(filepath)
    # arrays
    cue = data["cue"]
    cue = cue[np.where(cue != 0)[0]].dropna()

    lick = data["lick"].dropna().to_numpy()

    basename = os.path.basename(filepath)  # select basename for creating new csv fileE
    basename = basename.split(".")[0]  # split basename at . to add extension
    new_name = os.path.join(
        path_to_aligned_events, basename + "_licks_aligned_to_cue.csv"
    )  # assign new name

    # align each cue to 0 timepoint and
    licks_dict = {}
    for i in range(cue.shape[0]):
        arr_licks = np.array(lick - cue[i])
        licks_dict[i] = arr_licks
        df = pd.DataFrame.from_dict(licks_dict)
        df.to_csv(new_name, index=False, header=True)
    print(basename + " file saved")


# iterate over files in path_to_files to get discrete cue alignments and sae csv file for each in designated output path
all_licks = []
for f in os.scandir(path_to_files):
    if f.is_file():
        licks = align_trials(f, path_to_aligned_events)
        all_licks.append(licks)
print("all aligned event files saved")


def lick_freq(filepath):
    df = pd.read_csv(filepath)  # read csv
    arr = df[(df > -10) & (df < 20)].to_numpy()  #
    arr = arr[np.logical_not(np.isnan(arr))]
    lick_freq = np.histogram(arr, bins=155)[0] / len(df.columns)
    lick_freq = lick_freq * 5  # convert lick freq to licks/sec
    return lick_freq


lick_freq_dict = {}
for f in os.scandir(
    path_to_aligned_events
):  # path is to folder containing aligned event csvs.
    basename2 = os.path.basename(f)  # select basename for creating new csv fileE
    mouse_id = basename2.split("_")[0]  # split basename at _ to add extension
    if f.is_file():
        freq = lick_freq(f)
        lick_freq_dict[mouse_id] = freq


lick_freq_df = pd.DataFrame.from_dict(lick_freq_dict)

lick_freq_df = lick_freq_df.assign(
    mean=lick_freq_df.mean(
        axis=1
    ),  #  add mean, standered dev and x-axis time to dataframe
    std=lick_freq_df.std(axis=1),
    time_sec=np.arange(-10, 21, 0.2),
    sem=lick_freq_df.sem(axis=1),
)

lick_freq_df = lick_freq_df.assign(
    mean_smooth=lick_freq_df["mean"].rolling(window=5, center=True).mean(),
    std_smooth=lick_freq_df["std"].rolling(window=5, center=True).mean(),
    sem_smooth=lick_freq_df["sem"].rolling(window=5, center=True).mean(),
)

# save df as csv -> dayX_lick_frequency
lick_freq_df.to_csv(
    os.path.join(path_to_analyzed_data + "\\" + day_name + "_lick_frequency.csv"),
    index=False,
    header=True,
)
print("lick frequency file saved")

#  function to read read csv files in folder and concatenate all trials into one csv and save
df_all_trials = pd.DataFrame()
for f in os.scandir(path_to_aligned_events):
    df_f = pd.read_csv(f)
    df_all_trials = pd.concat([df_all_trials, df_f], axis=1)
df_all_trials.to_csv(
    os.path.join(path_to_analyzed_data + "\\" + day_name + "_all_trials.csv"),
    index=False,
    header=True,
)
print("compiled trials file saved")
print("preprocessing complete")

#%%

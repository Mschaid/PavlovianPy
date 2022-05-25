import pandas as pd
import os
import glob
import re
import numpy as np
import pavlovian_functions as pv

# path where guppy output files for day  are
path_to_files = r"R:\Mike\LHA_dopamine\LH_NAC_Headfix_FP\Photometry\Pav Training\2_color_pav\Sucrose_to_sucralose\Training\Day_4"

day = re.search(r"Day_\d\d?", path_to_files)[0]

# new directory for where time stamps will be saved
extracted_ts_path = (path_to_files + f"\\{day}_extracted_timestamps")
aligned_ts_path = (path_to_files + f"\\{day}_aligned_events")
analyzed_behavior_path = (path_to_files + f"\\{day}_analyzed_behavior")
tidy_analysis = (path_to_files + f"\\{day}_tidy_analysis")

# list of new dirs to create
new_folders = [extracted_ts_path, aligned_ts_path, analyzed_behavior_path, tidy_analysis]
#create new dirs (new_folders)  in path to files
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
        if len(event_dict.keys()) != len(events):
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


# function to calculate mean frequency of event and convert to dataframe
def group_freq_df(recording: str, filepath_list):
    freq_dict = {}
    for f in filepath_list:
        mouse_id = os.path.basename(f).split("_")[0]
        freq_arr = pv.calc_frequency(f)
        freq_dict[mouse_id] = freq_arr
        if len(freq_dict.keys()) != len(filepath_list):
            pass
        else:
            df = pd.DataFrame.from_dict(freq_dict)
#create dataframe from filepath and pair with event name
            group_df = (
                df
                    .assign(
                    mean=df.mean(axis=1),  # add mean,
                    time_sec=np.arange(-10, 21, 0.2),  # add time column
                    recording=recording,
                    day=(day.split('_')[1]))
                    .melt(id_vars=['day', 'time_sec','recording'], var_name='mouse', value_name='avg_frequency')
            )
            return recording, group_df


# create event name pair with dataframe
licks_analyzed = group_freq_df('licks', lick_files)
encoder_analyzed = group_freq_df('enconder', encoder_files)

# combine in list to loop and save seperately as csvs
all_analysis = [licks_analyzed, encoder_analyzed]
for i in all_analysis:
    i[1].to_csv(f"{analyzed_behavior_path}\\{day}_group_{i[0]}_analysis.csv",
                index=False)

# create list of dataframes, concatenate into master file and save
all_analysis_df_ony=[licks_analyzed[1], encoder_analyzed[1]]
group_behavior_tidy = pd.concat(all_analysis_df_ony)
# save dataframe as h5 and use event name in filename
group_behavior_tidy.to_hdf(f'{tidy_analysis}\\{day}_tidy_behavior.h5', key='behavior')

print('behavior analyzed')


"""
this section cleans photometry data and formats it into tidy data, saves as csv

"""
group_path = f'{path_to_files}\\average'  # get path to guppy group analysis 'average'
all_output_files = pv.list_subdirs(group_path)  # get list of all files in 'average'

fp_regex = '(cue|reward)_(GCAMP|RDA)[A-Z]{3}_z_score_(GCAMP|RDA)[A-Z]{3}.h5'  # regex pattern to parse files

all_fp_filepaths = [f for f in all_output_files if
                    re.match(fp_regex, os.path.basename(f))]  # create list of all relavent fp files.


#  function to clean data and format for tidy format
def clean_fp_data(path):
    day_numb = (re.search(('Day_\d'), path)[0]).split('_')[-1]
    sensor = re.search('GCAMP|RDA', path)[0]
    region = re.search('NAC|LHA', path)[0]
    event = re.search('cue|reward', path)[0]

    df = pd.read_hdf(path)
    df_clean = (
        df
            .assign(day=day_numb)
            .rename(columns=lambda c: c.split('-')[0])
            .drop(columns=['err'])
            .melt(id_vars=['day', 'timestamps'], var_name='mouse', value_name='z-score')
            .assign(sensor=sensor,
                    region=region,
                    event=event,
                    recording='photometry')
    )
    return df_clean

# applys clean function to all fp data, then concatenates and saves as h5 file
df_to_concat= [clean_fp_data(f) for f in all_fp_filepaths]
group_df = pd.concat(df_to_concat)
group_df.to_hdf(f'{tidy_analysis}\\{day}_tidy_photometry.h5', key='photometry')
print('fp data cleaned grouped and saved')



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
# %%
# path where guppy output files for day  are
path_to_files = r"R:\Mike\LHA_dopamine\LH_NAC_Headfix_FP\Photometry\Pav Training\2_color_pav\Sucrose_to_sucralose\Training\Day_8"

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
print('Directories created, extracting timestamps')
#  search path_to_files for all directories, then find subdirs that contain 'output' - append paths to list mouse_dirs
mouse_dirs = glob.glob(path_to_files + "\**\*output_*")
event_ts = ["Cuet", "Rwrp", "Lick", "endr"]
suffix = ".hdf5"
event_ts_suf = [i + suffix for i in event_ts]

for mouse in mouse_dirs:
    #  for each mouse output we will retrieve the file path for each event
    events = [pv.find_ts_file_path(mouse, event) for event in event_ts_suf]

    # create a dictionary where each event name is paired with the timestamp array
    event_dict = {}
    for event in events:
        event_id = os.path.basename(event).split(".")[0]
        event_ts_arr = pv.read_timestamps(event)
        event_dict[event_id] = event_ts_arr
        if len(event_dict.keys()) != len(events):
            pass
        else:
            # covert dict to df, pull mouse ID from path name and save as csv in extracted timestamps folder
            df_raw_ts = pd.DataFrame(
                dict([(k, pd.Series(v)) for k, v in event_dict.items()]))
            df_align_licks_to_cue = pv.align_events(df_raw_ts, "Cuet", "Lick")
            df_align_encoder_to_cue = pv.align_events(
                df_raw_ts, "Cuet", "endr")

            mouse_id = os.path.basename(mouse).split("-")[0]
            df_raw_ts = df_raw_ts.rename(columns={
                                         'Lick': 'lick', 'Cuet': 'cue', 'endr': 'encoder', 'Rwrp': 'reward'})
            df_raw_ts.to_csv(
                f"{extracted_ts_path}\\{mouse_id}_{day}_timestamps.csv", index=False)
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


def group_freq_df(recording: str, filepath_list):  # recording: str,
    freq_dict = {}
    for f in filepath_list:
        mouse_id = os.path.basename(f).split("_")[0]
        freq_arr = pv.calc_frequency(f)
        freq_dict[mouse_id] = freq_arr
        if len(freq_dict.keys()) != len(filepath_list):
            pass
        else:
            df = pd.DataFrame.from_dict(freq_dict)
# create dataframe from filepath and pair with event name
            group_behavior_df = (
                df
                .rolling(window=2, center=True).mean()
                .assign(
                    # mean=df.mean(axis=1),  # add mean,
                    time_sec=np.arange(-10, 21, 0.2),  # add time column
                    recording=recording,
                    day=(day.split('_')[1]))
                .dropna()
                .melt(id_vars=['day', 'time_sec', 'recording'], var_name='mouse', value_name='avg_frequency')
            )
            # print(group_behavior_df)
    return recording, group_behavior_df


# create event name pair with dataframe
licks_analyzed = group_freq_df('lick', lick_files)
encoder_analyzed = group_freq_df('encoder', encoder_files)

# combine in list to loop and save seperately as csvs
all_analysis = [licks_analyzed, encoder_analyzed]
for i in all_analysis:
    i[1].to_csv(f"{analyzed_behavior_path}\\{day}_group_{i[0]}_analysis.csv",
                index=False)

# create list of dataframes, concatenate into master file and save
all_analysis_df_ony = [licks_analyzed[1], encoder_analyzed[1]]
group_behavior_tidy = pd.concat(all_analysis_df_ony)

# save dataframe as h5 and use event name in filename
group_behavior_path = f'{tidy_analysis}\\{day}_tidy_behavior.h5'
group_behavior_tidy.to_hdf(group_behavior_path, key='behavior')

print('behavior analyzed')
"""
this section cleans photometry data and formats it into tidy data, saves as h5 or csv 

"""
group_path = f'{path_to_files}\\average'  # get path to guppy group analysis 'average'
# get list of all files in 'average'
all_output_files = pv.list_subdirs(group_path)

# regex pattern to parse files
fp_regex = '(cue|reward)_(GCAMP|RDA)[A-Z]{3}_z_score_(GCAMP|RDA)[A-Z]{3}.h5'
# create list of all relavent fp files.
all_fp_filepaths = [f for f in all_output_files if
                    re.match(fp_regex, os.path.basename(f))]


#  function to clean data and format for tidy format
def clean_fp_data(path):
    day_numb = (re.search(('Day_\d'), path)[0]).split('_')[-1]
    sensor = re.search('GCAMP|RDA', os.path.basename(path))[0]
    region = re.search('NAC|LHA', os.path.basename(path))[0]
    event = re.search('cue|reward', os.path.basename(path))[0]

    df = pd.read_hdf(path)
    time_stamps = df['timestamps']
    df_clean = (
        df
        .drop(['timestamps'], axis=1)
        .rolling(window=500, center=True).mean()
        .assign(day=day_numb)
        .rename(columns=lambda c: c.split('-')[0])
        .drop(columns=['err'])
        .assign(time_stamps=time_stamps)
        .dropna()
        .melt(id_vars=['day', 'time_stamps'], var_name='mouse', value_name='z-score')
        .assign(sensor=sensor,
                region=region,
                event=event,
                recording='photometry')
    )
    return df_clean

# function to clean AUC data and save


def clean_AUC_data(path):
    day_numb = (re.search(('Day_\d'), path)[0]).split('_')[-1]
    sensor = re.search('GCAMP|RDA', os.path.basename(path))[0]
    region = re.search('NAC|LHA', os.path.basename(path))[0]
    event = re.search('cue|reward', os.path.basename(path))[0]

    df = pd.read_csv(path)
    AUC_clean = (
        df
        .assign(mouse=df['Unnamed: 0'].str.split('-', expand=True)[0],
                trial=df['Unnamed: 0'].str.split('_', expand=True)[1])
        .drop(columns='Unnamed: 0')
        .melt(id_vars=['mouse', 'trial'], var_name='category', value_name='value')
        .assign(sensor=sensor,
                region=region,
                event=event,
                day=day_numb,
                recording='photometry')
    )
    return AUC_clean


# applys clean function to all fp data, then concatenates and saves as h5 file
df_to_concat = [clean_fp_data(f) for f in all_fp_filepaths]
df_to_concat[0]


group_fp = pd.concat(df_to_concat)
group_fp_path = f'{tidy_analysis}\\{day}_tidy_photometry.h5'
group_fp.to_hdf(group_fp_path, key='photometry')
print('fp data cleaned grouped and saved')


peak_auc_regex = fp_regex = 'peak_AUC_(cue|reward)_(GCAMP|RDA)[A-Z]{3}_z_score_(GCAMP|RDA)[A-Z]{3}.csv'
all_peak_AUC_filepaths = [f for f in all_output_files if
                          re.match(peak_auc_regex, os.path.basename(f))]


# applys clean function to all fp AUC data, then concatenates and saves as h5 file

auc_df_to_concat = [clean_AUC_data(f) for f in all_peak_AUC_filepaths]
group_AUC_df = pd.concat(auc_df_to_concat)
group_AUC_path = f'{tidy_analysis}\\{day}_tidy_AUC_photometry.h5'
group_AUC_df.to_hdf(group_AUC_path, key='peak_AUC')
print('AUC data cleaned grouped and saved')


def agg_and_clean_fp(df):  # function to group and aggreate fp data

    group_by = ['time_stamps', 'sensor', 'region', 'event']
    agg_dict = {'z-score': ['mean', 'std', 'sem']}

    df = (
        df
        .reset_index()
        .drop(['index'], axis=1)
        .groupby(by=group_by)
        .agg(agg_dict)
        .pipe(pv.flatten_df)
    )
    return df


def drop_mice(df):  # filteres dataframe prior to group and aggreation

    filtered_df = df[(df.mouse != '512581') &
                     (df.mouse != '514957') &
                     #  (df.mouse != '514958') &
                     (df.mouse != 'mean')
                     ]
    return filtered_df


"""
Final photometry dataframe for plotting 
"""
all_fp_df = (group_fp.pipe(agg_and_clean_fp))  # all mice

nac_fp_df = (group_fp  # dropped missing nac probe mice
             .pipe(drop_mice)
             .pipe(agg_and_clean_fp)
             )


"""
group and aggregate behavior 
"""

behavior_group_by = ['time_sec', 'recording']
behavior_agg_dict = {'avg_frequency': ['mean', 'std', 'sem']}

#
group_behavior_tidy = (
    group_behavior_tidy
    .reset_index()
    .drop(['index'], axis=1)
    .groupby(by=behavior_group_by)
    .agg(behavior_agg_dict)
    .pipe(pv.flatten_df)
)
group_behavior_tidy


def fp_plot_line(df, sensor=None, region=None, event=None, sub_axes=None, alpha=None, color=None, linewidth=None):

    data = df[(df.sensor == sensor)
              & (df.region == region)
              & (df.event == event)
              ]

    sns.lineplot(data=data,
                 x='time_stamps',
                 y='z-score_mean',
                 color=color,
                 linewidth=linewidth,
                 ax=sub_axes
                 )
    sub_axes.fill_between(data=data, x=data['time_stamps'], y1=(data['z-score_mean'] + data['z-score_sem']),
                          y2=(data['z-score_mean'] - data['z-score_sem']), color=color, alpha=alpha, linewidth=0)


def behavior_plot_line(df, recording=None, sub_axes=None, alpha=None, color=None, linewidth=None):

    data = df[(df.recording == recording)]

    sns.lineplot(data=data,
                 x='time_sec',
                 y='avg_frequency_mean',
                 color=color,
                 linewidth=linewidth,
                 ax=sub_axes
                 )
    sub_axes.fill_between(data=data, x=data['time_sec'], y1=(data['avg_frequency_mean'] + data['avg_frequency_sem']),
                          y2=(data['avg_frequency_mean'] - data['avg_frequency_sem']), color=color, alpha=alpha, linewidth=0)


def draw_cue_box(ax):
    #  draw box on plot for cue
    rect = patches.Rectangle(
        (0, -2), width=5, height=10, alpha=0.25, facecolor="lightgrey")
    ax.add_patch(rect)


print('preprocessing complete, ready to plot')
#
# %%

fig = plt.figure(constrained_layout=True, figsize=(10, 10))

gs = GridSpec(3, 4, figure=fig)

fig.text(0.25, 0.95,
         'NAC|Cue',
         #  style = 'italic',
         fontsize=10,
         color="black")

ax1 = fig.add_subplot(gs[0, 0])

fp_plot_line(df=nac_fp_df, sensor='GCAMP', region='NAC', event='cue',
             alpha=0.25, color='lime', linewidth=0.5, sub_axes=ax1)
sns.despine(top=True, right=True, ax=ax1)
ax1.set_xlim(left=-5, right=15)  # x axis range
# axs.set_ylim(bottom=-0.5, top=2.5)  # y axis range
ax1.tick_params(axis="both", which="major", labelsize=8)  # set tick label size
ax1.set_xlabel("Time(sec)", fontsize=8)  # x axis label
ax1.set_ylabel("z-score", fontsize=8)  # y axis label
ax1.set_box_aspect(1)


ax2 = fig.add_subplot(gs[0, 1])

fp_plot_line(df=nac_fp_df, sensor='RDA', region='NAC', event='cue',
             alpha=0.25, color='red', linewidth=0.5, sub_axes=ax2)
sns.despine(top=True, right=True, ax=ax2)
ax2.set_xlim(left=-5, right=15)  # x axis range
# axs.set_ylim(bottom=-0.5, top=2.5)  # y axis range
ax2.tick_params(axis="both", which="major", labelsize=8)  # set tick label size
ax2.set_xlabel("Time(sec)", fontsize=8)  # x axis label
ax2.set_ylabel("z-score", fontsize=8)  # y axis label
ax2.set_box_aspect(1)


fig.text(0.25, 0.6,
         'LHA|Cue',
         #  style = 'italic',
         fontsize=10,
         color="black")

ax3 = fig.add_subplot(gs[1, 0])

fp_plot_line(df=all_fp_df, sensor='GCAMP', region='LHA', event='cue',
             alpha=0.25, color='lime', linewidth=0.5, sub_axes=ax3)
sns.despine(top=True, right=True, ax=ax3)
ax3.set_xlim(left=-5, right=15)  # x axis range
# axs.set_ylim(bottom=-0.5, top=2.5)  # y axis range
ax3.tick_params(axis="both", which="major", labelsize=8)  # set tick label size
ax3.set_xlabel("Time(sec)", fontsize=8)  # x axis label
ax3.set_ylabel("z-score", fontsize=8)  # y axis label
ax3.set_box_aspect(1)


ax4 = fig.add_subplot(gs[1, 1])

fp_plot_line(df=all_fp_df, sensor='RDA', region='LHA', event='cue',
             alpha=0.25, color='red', linewidth=0.5, sub_axes=ax4)
sns.despine(top=True, right=True, ax=ax4)
ax4.set_xlim(left=-5, right=15)  # x axis range
# axs.set_ylim(bottom=-0.5, top=2.5)  # y axis range
ax4.tick_params(axis="both", which="major", labelsize=8)  # set tick label size
ax4.set_xlabel("Time(sec)", fontsize=8)  # x axis label
ax4.set_ylabel("z-score", fontsize=8)  # y axis label
ax4.set_box_aspect(1)


ax5 = fig.add_subplot(gs[2, 0])
behavior_plot_line(group_behavior_tidy, recording='lick',
                   sub_axes=ax5, alpha=0.5, color='black', linewidth=0.5)
sns.despine(top=True, right=True, ax=ax5)
ax5.set_xlim(left=-5, right=15)
# ax5.set_ylim(bottom=-0.5, top=1)
ax5.set_xlabel("Time(sec)", fontsize=8)
ax5.set_ylabel('Lick frequency', fontsize=8)  # x axis range
ax5.set_box_aspect(1)

ax6 = fig.add_subplot(gs[2, 1])
behavior_plot_line(group_behavior_tidy, recording='encoder',
                   sub_axes=ax6, alpha=0.5, color='black', linewidth=0.5)
sns.despine(top=True, right=True, ax=ax6)
ax6.set_xlim(left=-5, right=15)
# ax6.set_ylim(bottom=-0.5, top=1)
ax6.set_xlabel("Time(sec)", fontsize=8)
ax6.set_ylabel('encoder', fontsize=8)  # x axis range
ax6.set_box_aspect(1)


# ax4 = fig.add_subplot(gs[-1, 0])
# ax5 = fig.add_subplot(gs[-1, -2])

# fig.suptitle("GridSpec")
# format_axes(fig)

plt.show()


# %%

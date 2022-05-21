# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import os
import glob


path_to_analyzed_data = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day10\day10_csv_timestamps_analyzed_behavior_data'
path_to_NAc_Cue =r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day10\average\cue_NAC_z_score_NAC.h5'
# import all trials csv into dataframe
for file in glob.glob(os.path.join(path_to_analyzed_data, '*_all_trials.csv')):
    df_all_trials= pd.read_csv(file)

# import lick frequency trials csv into dataframe
for file in glob.glob(os.path.join(path_to_analyzed_data, '*_lick_frequency.csv')):
    df_lick_freq = pd.read_csv(file)

#read photometry PSTH plots

NAc_cue_df = pd.read_hdf(path_to_NAc_Cue)
NAc_cue_df = NAc_cue_df.iloc[::2,:] # downsample FP data

df_all_trials_T = df_all_trials.fillna(-50000).T

#create new arrays from dataframe
all_trials_arr = np.array(df_all_trials_T)

#%%
#smooth FP data
# NAc_cue_df = NAc_cue_df.assign(mean_smooth = NAc_cue_df['mean'].rolling(window = 500, center=True).mean(),
#                                err_smooth = NAc_cue_df['err'].rolling(window = 500, center=True).mean()
#                                )
#%%
#  makes figure
fig, axs = plt.subplots(nrows=3,
                        ncols=1,
                        sharex=True,
                        squeeze=True,
                        figsize=(3, 3))  # sets # of plots columns x ros

fig.suptitle('Day 10', fontsize=12)  # figure title
fig.align_ylabels()

#photometry plot for NAc cue
#mean line and axs
sns.lineplot(data = NAc_cue_df,
             x='timestamps',
             y='mean',
             linewidth = 0.2,
             color='g',
             ax=axs[0])
#fill error
axs[0].fill_between(NAc_cue_df['timestamps'],
                    (NAc_cue_df['mean']+NAc_cue_df['err']),
                    (NAc_cue_df['mean']-NAc_cue_df['err']),
                    color='g',
                    alpha=0.3,
                    linewidth=0)
axs[0].set_xlim(left=-5, right=15) # x axis range
axs[0].set_ylim(bottom=-0.5, top=2.5) # y axis range
axs[0].set_xlabel('Time(sec)') #x axis label
axs[0].set_ylabel('z-score') #y axis label
axs[0].set_box_aspect(0.5) #plot size
sns.despine(ax=axs[0]) #remove box outline

#draw box on plot for cue
rect = patches.Rectangle((0,-0.5),
                         width=5,
                         height=3,
                         alpha=0.15,
                         facecolor = 'lightcoral',
                         axes=axs[0])
axs[0].add_patch(rect)
# raster plot for second panel
axs[1].eventplot(all_trials_arr,
                 orientation='horizontal',
                 color='k',
                 linelengths=1,
                 linewidth=.2,
                 rasterized=True)

sns.despine(ax=axs[1],
            top=True,
            right=True,
            left=True,
            bottom=True,
            offset=None,
            trim=False)
axs[1].set_box_aspect(.5)  # size of plot
axs[1].set_xlim(left=-5, right=15)  # time frame of xaxi
# axs[1].axvline(x=5, color='k', linewidth=0.5, linestyle='-')  # line for reward
axs[1].xaxis.set_visible(False)  # hide x ticks
axs[1].set_ylabel('Trial')  # y axis label
#draw box on plot for cue
rect = patches.Rectangle((0,0),
                         width=5,
                         height=600,
                         alpha=0.15,
                         facecolor = 'lightcoral',
                         axes=axs[1])
axs[1].add_patch(rect)

#lineplot of lick frequency
sns.lineplot(ax=axs[2],
             data = df_lick_freq,
             x='time_sec',
             y='mean_smooth',
             color='k',
             linewidth=0.2,
             legend=False)
# df_lick_freq.plot(ax=axs[1], x='time_sec', y=['436302','436302'], legend=False, linewidth = 0.2)
axs[2].fill_between(df_lick_freq['time_sec'],
                    (df_lick_freq['mean_smooth']+df_lick_freq['sem_smooth']), #SEM
                    (df_lick_freq['mean_smooth']-df_lick_freq['sem_smooth']),#SEM
                    color='k',
                    alpha=0.3,
                    linewidth=0)
#remove spines
sns.despine(ax=axs[2],
            top=True,
            right=True,
            offset=None,
            trim=False)
axs[2].set_box_aspect(.5)  # size of plot
axs[2].set_xlim(left=-5, right=15)
axs[2].set_ylabel('lick rate\n(licks/sec)') # y axis label
axs[2].set_xlabel('time(sec)')  # x axis label
#draw box on plot for cue
rect = patches.Rectangle((0,0),
                         width=5,
                         height=600,
                         alpha=0.15,
                         facecolor='lightcoral',
                         axes=axs[2])
axs[2].add_patch(rect)

plt.tight_layout()
plt.rcParams['svg.fonttype'] = 'none' #save text as text in svg
plt.savefig(path_to_analyzed_data+'\\day_10_behavior_NAcCue.tiff',
            dpi=300,
            transparent=True)
plt.savefig(path_to_analyzed_data+'\\day_10_behavior_NAcCue.svg',
            dpi=300,
            transparent=True)
plt.show()





#%%


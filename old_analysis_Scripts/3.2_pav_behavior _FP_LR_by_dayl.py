
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import os
import glob


#Day1 paths (day 4 for cohort 2)
NAc_Cue_D1 = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day4\average\cue_NAC_z_score_NAC.h5'
LH_Cue_D1 = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day4\average\cue_LH_z_score_LH.h5'
lick_freq_D1 = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day4\day4_csv_timestamps_analyzed_behavior_data\day4_lick_frequency.csv'

#Day5 paths (day 9 for cohort 2)
NAc_Cue_D5 = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day9\average\cue_NAC_z_score_NAC.h5'
LH_Cue_D5 = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day9\average\cue_LH_z_score_LH.h5'
lick_freq_D5 = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day9\day9_licks_behavior_analyzed_behavior_data\day9_lick_frequency.csv'
#Day10 paths (day 14 for cohort 2)
NAc_Cue_D10 = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day13\average\cue_NAC_z_score_NAC.h5'
LH_Cue_D10 = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day13\average\cue_LH_z_score_LH.h5'
lick_freq_D10= r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day13\day13_csv_timestamps_analyzed_behavior_data\day13_lick_frequency.csv'

path_to_save = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\time_course_plots'
#%%

#  read, downsample, smoothphotometry PSTH plots and read lick freq ito dataframes

#D1
NAc_Cue_D1_df = pd.read_hdf(NAc_Cue_D1)
NAc_Cue_D1_df = NAc_Cue_D1_df.iloc[::2,:].rolling(window=250, center = True).mean() # downsample and rolling average FP data
LH_Cue_D1_df = pd.read_hdf(LH_Cue_D1)
LH_Cue_D1_df = LH_Cue_D1_df.iloc[::2,:].rolling(window=250, center = True).mean()# downsample and rolling average FP data
lick_freq_D1_df = pd.read_csv(lick_freq_D1)
#D5
NAc_Cue_D5_df = pd.read_hdf(NAc_Cue_D5)
NAc_Cue_D5_df = NAc_Cue_D5_df.iloc[::2,:].rolling(window=250, center = True).mean() # downsample and rolling average FP data
LH_Cue_D5_df = pd.read_hdf(LH_Cue_D5)
LH_Cue_D5_df = LH_Cue_D5_df.iloc[::2,:].rolling(window=250, center = True).mean()# downsample and rolling average FP data
lick_freq_D5_df = pd.read_csv(lick_freq_D5)
#D10
NAc_Cue_D10_df = pd.read_hdf(NAc_Cue_D10)
NAc_Cue_D10_df = NAc_Cue_D10_df.iloc[::2,:].rolling(window=250, center = True).mean() # downsample and rolling average FP data
LH_Cue_D10_df = pd.read_hdf(LH_Cue_D10)
LH_Cue_D10_df = LH_Cue_D10_df.iloc[::2,:].rolling(window=250, center = True).mean()# downsample and rolling average FP data
lick_freq_D10_df = pd.read_csv(lick_freq_D10)

#%%
#  makes figure
fig, axs = plt.subplots(nrows=1,
                        ncols=3,
                        squeeze=True,
                        figsize=(5,5)
                        )  # sets # of plots columns x ros


day1_color = 'black'
day5_color = 'deepskyblue'
day10_color = 'crimson'
cue_color = 'lightyellow'
label_pad = 2
#  photometry plot for NAc cue
#  mean line and axs
sns.lineplot(data=NAc_Cue_D1_df, #day1
             x='timestamps',
             y='mean',
             linewidth=0.2,
             color=day1_color,
             ax=axs[0])
sns.lineplot(data=NAc_Cue_D5_df, #day5
             x='timestamps',
             y='mean',
             linewidth=0.2,
             color=day5_color,
             ax=axs[0])
sns.lineplot(data=NAc_Cue_D10_df, #day10
             x='timestamps',
             y='mean',
             linewidth=0.2,
             color=day10_color,
             ax=axs[0])
# #  fill error
axs[0].fill_between(NAc_Cue_D1_df['timestamps'], #day1
                    (NAc_Cue_D1_df['mean']+NAc_Cue_D1_df['err']),
                    (NAc_Cue_D1_df['mean']-NAc_Cue_D1_df['err']),
                    color=day1_color,
                    alpha=0.3,
                    linewidth=0)
axs[0].fill_between(NAc_Cue_D5_df['timestamps'], #day5
                    (NAc_Cue_D5_df['mean']+NAc_Cue_D5_df['err']),
                    (NAc_Cue_D5_df['mean']-NAc_Cue_D5_df['err']),
                    color=day5_color,
                    alpha=0.3,
                    linewidth=0)
axs[0].fill_between(NAc_Cue_D10_df['timestamps'], #day10
                    (NAc_Cue_D10_df['mean']+NAc_Cue_D10_df['err']),
                    (NAc_Cue_D10_df['mean']-NAc_Cue_D10_df['err']),
                    color=day10_color,
                    alpha=0.3,
                    linewidth=0)
axs[0].set_xlim(left=-5, right=15) # x axis range
axs[0].set_xticks([0,5,10])
axs[0].set_ylim(bottom=-0.5, top=2.5)# y axis range
axs[0].set_yticks([0,1,2])
axs[0].tick_params(axis='both', which='major', labelsize=8) # set tick label size
axs[0].set_xlabel('Time(sec)',fontsize = 8, labelpad=label_pad) #    x axis label
axs[0].set_ylabel('z-score', fontsize = 8, labelpad=label_pad) #y axis label
axs[0].set_box_aspect(1) #  plot size
sns.despine(ax=axs[0]) #  remove box outline
axs[0].set_title('NAc Dopamine', fontsize=8)
# 
# #  draw box on plot for cue
rect = patches.Rectangle((0, -0.5),
                         width=5,
                         height=3,
                         alpha=0.5,
                         facecolor=cue_color,
                         axes=axs[0])
axs[0].add_patch(rect)


# # plot for LH_cue_FP
#  photometry plot for NAc cue
#  mean line and axs
sns.lineplot(data=LH_Cue_D1_df, #day1
             x='timestamps',
             y='mean',
             linewidth=0.2,
             color=day1_color,
             ax=axs[1])
sns.lineplot(data=LH_Cue_D5_df, #day5
             x='timestamps',
             y='mean',
             linewidth=0.2,
             color=day5_color,
             ax=axs[1])
sns.lineplot(data=LH_Cue_D10_df, #day10
             x='timestamps',
             y='mean',
             linewidth=0.2,
             color=day10_color,
             ax=axs[1])
# #  fill error
axs[1].fill_between(LH_Cue_D1_df['timestamps'], #day1
                    (LH_Cue_D1_df['mean']+LH_Cue_D1_df['err']),
                    (LH_Cue_D1_df['mean']-LH_Cue_D1_df['err']),
                    color=day1_color,
                    alpha=0.3,
                    linewidth=0)
axs[1].fill_between(LH_Cue_D5_df['timestamps'], #day5
                    (LH_Cue_D5_df['mean']+LH_Cue_D5_df['err']),
                    (LH_Cue_D5_df['mean']-LH_Cue_D5_df['err']),
                    color=day5_color,
                    alpha=0.3,
                    linewidth=0)
axs[1].fill_between(LH_Cue_D10_df['timestamps'], #day10
                    (LH_Cue_D10_df['mean']+LH_Cue_D10_df['err']),
                    (LH_Cue_D10_df['mean']-LH_Cue_D10_df['err']),
                    color=day10_color,
                    alpha=0.3,
                    linewidth=0)
axs[1].set_xlim(left=-5, right=15) # x axis range
axs[1].set_xticks([0,5,10])
axs[1].set_ylim(bottom=-0.125, top=0.6)
axs[1].set_yticks([0,0.25,0.5])# y axis range
axs[1].locator_params(axis="x", nbins=3) # number of x axis ticks
axs[1].locator_params(axis="y", nbins=3)# number of y axis ticks
axs[1].tick_params(axis='both', which='major', labelsize=8) # set tick label size
axs[1].set_xlabel('Time(sec)',fontsize = 8, labelpad=label_pad) #    x axis label
axs[1].set_ylabel('z-score', fontsize = 8, labelpad=label_pad) #y axis label
axs[1].set_box_aspect(1) #  plot size
sns.despine(ax=axs[1]) #  remove box outline
axs[1].set_title('LHA Dopamine', fontsize=8)
# 
# #  draw box on plot for cue
rect = patches.Rectangle((0, -0.5),
                         width=5,
                         height=3,
                         alpha=0.5,
                         facecolor=cue_color,
                         axes=axs[1])
axs[1].add_patch(rect)
# 
# #lineplot of lick frequency
sns.lineplot(ax=axs[2],
             data = lick_freq_D1_df,
             x='time_sec',
             y='mean_smooth',
             color=day1_color,
             linewidth=0.2,
             legend=False)
sns.lineplot(ax=axs[2],
             data = lick_freq_D5_df,
             x='time_sec',
             y='mean_smooth',
             color=day5_color,
             linewidth=0.2,
             legend=False)
sns.lineplot(ax=axs[2],
             data = lick_freq_D10_df,
             x='time_sec',
             y='mean_smooth',
             color=day10_color,
             linewidth=0.2,
             legend=False)
axs[2].fill_between(lick_freq_D1_df['time_sec'],
                    (lick_freq_D1_df['mean_smooth']+lick_freq_D1_df['sem_smooth']), #SEM
                    (lick_freq_D1_df['mean_smooth']-lick_freq_D1_df['sem_smooth']),#SEM
                    color=day1_color,
                    alpha=0.3,
                    linewidth=0)
axs[2].fill_between(lick_freq_D5_df['time_sec'],
                    (lick_freq_D5_df['mean_smooth']+lick_freq_D5_df['sem_smooth']), #SEM
                    (lick_freq_D5_df['mean_smooth']-lick_freq_D5_df['sem_smooth']),#SEM
                    color=day5_color,
                    alpha=0.3,
                    linewidth=0)
axs[2].fill_between(lick_freq_D10_df['time_sec'],
                    (lick_freq_D10_df['mean_smooth']+lick_freq_D10_df['sem_smooth']), #SEM
                    (lick_freq_D10_df['mean_smooth']-lick_freq_D10_df['sem_smooth']),#SEM
                    color=day10_color,
                    alpha=0.3,
                    linewidth=0)
# #remove spines
sns.despine(ax=axs[2],
            top=True,
            right=True,
            offset=None,
            trim=False)
axs[2].set_box_aspect(1)  # size of plot

axs[2].set_xlim(left=-5, right=15)
axs[2].set_xticks([0,5,10])
axs[2].set_xlabel('Time(sec)', fontsize = 8, labelpad=label_pad)  # x axis label

axs[2].set_ylim(bottom=-1, top=7)
axs[2].set_yticks([0,3,6])
axs[2].set_ylabel('lick rate\n(licks/sec)',  fontsize = 8, labelpad=label_pad) # y axis label

axs[2].tick_params(axis='both', which='major', labelsize=8) # set tick label size



axs[2].set_title('Lick Rate', fontsize = 8)
# #draw box on plot for cue
rect = patches.Rectangle((-.5,0),
                         width=5,
                         height=8,
                         alpha=0.5,
                         facecolor=cue_color,
                         axes=axs[2])
axs[2].add_patch(rect)

# LEGEND
axs[0].text(-6,5.75, 'Day 1',
            horizontalalignment='left',
            verticalalignment='center',
            color = day1_color)
axs[0].text(-6,5, 'Day 5',
            horizontalalignment='left',
            verticalalignment='center',
            color = day5_color)
axs[0].text(-6,4.25, 'Day 10',
            horizontalalignment='left',
            verticalalignment='center',
            color = day10_color)

##plt param and save
plt.tight_layout()
plt.rcParams['svg.fonttype'] = 'none' #save text as text in svg
plt.savefig(path_to_save + '\\time_course_D1_5_10.tiff',
            dpi=300,
            transparent=True)
plt.savefig(path_to_save + '\\time_course_D1_5_10.svg',
            dpi=300,
            transparent=True)
plt.show()





#%%


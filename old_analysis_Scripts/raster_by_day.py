import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

d1_trials = pd.read_csv(r"R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_training\day4\day4_csv_timestamps_aligned_events\436302_day4_timestamps_licks_aligned_to_cue.csv")
d5_trials = pd.read_csv(r"R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_training\day9\day9_licks_behavior_aligned_events\436302_day9_licks_aligned_to_cue.csv")
d10_trials = pd.read_csv(r"R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_training\day13\day13_csv_timestamps_aligned_events\436302_day13_timestamps_licks_aligned_to_cue.csv")

df_all_trials = pd.concat([d1_trials, d5_trials, d10_trials], axis=1)
df_all_trials_T = df_all_trials.fillna(-50000).T
all_trials_arr = np.array(df_all_trials_T)
#%%
# raster plot for second panel
fig, axs = plt.subplots(
    squeeze=True,
    figsize=(1,1)
)# sets # of plots columns x ros


axs.eventplot(all_trials_arr,
                   orientation='horizontal',
                   color='k',
                   linelengths=1,
                   linewidth=.25,
                   rasterized=True)

sns.despine(ax=axs,
            top=True,
            right=True,
            left=True,
            bottom=True,
            offset=None,
            trim=False)
axs.set_box_aspect(1)  # size of plot
axs.set_xlim(left=-5, right=15)  # time frame of xaxi

axs.tick_params(axis='both', which='major', labelsize=8) # set tick label size
axs.set_xlabel('Time(sec)',fontsize = 8) #    x axis label
axs.set_xlim(left=-5, right=15) #  x axis limit
axs.set_xticks([0,5,10]) #  x axis tick label
axs.set_xlabel('Time(sec)', fontsize = 8, labelpad=2)  # x axis label
axs.set_ylim(bottom=0, top=90) # y axis limit
axs.set_yticks([15,45,75]) # y tick labels
axs.set_yticklabels(['Day 1','Day 5', ' Day 10']) # y tick labels


#draw box on plot for cue
rect = patches.Rectangle((0,0),
                         width=5,
                         height=100,
                         alpha=0.25,
                         facecolor = 'lightyellow',
                         axes=axs)
axs.add_patch(rect)
plt.rcParams['svg.fonttype'] = 'none' #save text as text in svg
plt.savefig(r'R:\Mike\Grants\NRSA F32\Figures' + '\\raster_by_day.svg', dpi=300)
plt.show()

#%%


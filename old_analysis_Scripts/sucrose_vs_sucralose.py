
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from scipy import stats
import os
import glob

#sucrose path
NAc_Cue_sucrose = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_training\day14\average\cue_NAC_z_score_NAC.h5'
LH_Cue_sucrose = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_training\day14\average\cue_LH_z_score_LH.h5'
lick_freq_sucrose = r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_training\day14\day14_csv_timestamps_analyzed_behavior_data\day14_lick_frequency.csv'

#sucralose paths (day 9 for cohort 2)
NAc_Cue_sucralose = r"R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_to_sucralose\day3\average\cue_NAC_z_score_NAC.h5"
LH_Cue_sucralose = r"R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_to_sucralose\day3\average\cue_LH_z_score_LH.h5"
lick_freq_sucralose = r"R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_to_sucralose\day3\day3_csv_timestamps_analyzed_behavior_data\day3_lick_frequency.csv"

path_to_save = r'R:\Mike\Grants\NRSA F32\Figures'

#  read, downsample, smoothphotometry PSTH plots and read lick freq ito dataframes
#sucrose
NAc_Cue_sucrose_df = pd.read_hdf(NAc_Cue_sucrose)
NAc_Cue_sucrose_df = NAc_Cue_sucrose_df.iloc[::2,:].rolling(window=250, center = True).mean() # downsample and rolling average FP data
LH_Cue_sucrose_df = pd.read_hdf(LH_Cue_sucrose)
LH_Cue_sucrose_df = LH_Cue_sucrose_df.iloc[::2,:].rolling(window=250, center = True).mean()# downsample and rolling average FP data
lick_freq_sucrose_df = pd.read_csv(lick_freq_sucrose)
#sucralose
NAc_Cue_sucralose_df = pd.read_hdf(NAc_Cue_sucralose)
NAc_Cue_sucralose_df = NAc_Cue_sucralose_df.iloc[::2,:].rolling(window=250, center = True).mean() # downsample and rolling average FP data
LH_Cue_sucralose_df = pd.read_hdf(LH_Cue_sucralose)
LH_Cue_sucralose_df = LH_Cue_sucralose_df.iloc[::2,:].rolling(window=250, center = True).mean()# downsample and rolling average FP data
lick_freq_sucralose_df = pd.read_csv(lick_freq_sucralose)

AUC_df = pd.read_csv(r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\lickrate_vs_AUC.csv')
AUC_df = AUC_df.assign(LHA_Cue_AUC_E3 = AUC_df['LHA_Cue_AUC']/1000,NAC_Cue_AUC_E3 = AUC_df['NAC_Cue _AUC']/1000)
AUC_df_NAC = AUC_df.dropna()

LHA_R = stats.pearsonr(AUC_df['lick rate'], AUC_df['LHA_Cue_AUC'])
LHA_R2 = (LHA_R[0]**2).round(3)
LHA_pval=LHA_R[1].round(3)

NAC_R = stats.pearsonr(AUC_df_NAC['lick rate'], AUC_df_NAC['NAC_Cue _AUC'])
NAC_R2 = (NAC_R[0]**2).round(3)
NAC_pval = NAC_R[1].round(3)


print('LHA R2 is ' + str(LHA_R2))
print('LHA p value is ' + str(LHA_pval))
print('NAC R2 is ' + str(NAC_R2))
print('NAC p value is ' + str(NAC_pval))
#%%  makes figure
fig, axs = plt.subplots(nrows=2,
                        ncols=3,
                        squeeze=True,
                        figsize=(5,5)
                        )  # sets # of plots columns x ros


sucrose_color = 'black'
sucralose_color = 'deepskyblue'
cue_color = 'lightyellow'
label_pad = 2
#  photometry plot for NAc cue
#  mean line and axs

# # plot for LH_cue_FP
#  photometry plot for NAc cue
#  mean line and axs
sns.lineplot(data=LH_Cue_sucrose_df, #sucrose
             x='timestamps',
             y='mean',
             linewidth=0.4,
             color=sucrose_color,
             ax=axs[0, 0])
sns.lineplot(data=LH_Cue_sucralose_df, #sucralose
             x='timestamps',
             y='mean',
             linewidth=0.4,
             color=sucralose_color,
             ax=axs[0, 0])

# #  fill error
axs[0, 0].fill_between(LH_Cue_sucrose_df['timestamps'], #sucrose
                    (LH_Cue_sucrose_df['mean']+LH_Cue_sucrose_df['err']),
                    (LH_Cue_sucrose_df['mean']-LH_Cue_sucrose_df['err']),
                    color=sucrose_color,
                    alpha=0.3,
                    linewidth=0)
axs[0, 0].fill_between(LH_Cue_sucralose_df['timestamps'], #sucralose
                    (LH_Cue_sucralose_df['mean']+LH_Cue_sucralose_df['err']),
                    (LH_Cue_sucralose_df['mean']-LH_Cue_sucralose_df['err']),
                    color=sucralose_color,
                    alpha=0.3,
                    linewidth=0)

axs[0, 0].set_xlim(left=-5, right=15) # x axis range
axs[0, 0].set_xticks([0,5,10])
axs[0, 0].set_ylim(bottom=-0.125, top=0.45)
axs[0, 0].set_yticks([0,0.2,0.4])# y axis range
axs[0, 0].locator_params(axis="x", nbins=3) # number of x axis ticks
axs[0, 0].locator_params(axis="y", nbins=3)# number of y axis ticks
axs[0, 0].tick_params(axis='both', which='major', labelsize=8) # set tick label size
axs[0, 0].set_xlabel('Time(sec)',fontsize = 8, labelpad=label_pad) #    x axis label
axs[0, 0].set_ylabel('z-score', fontsize = 8, labelpad=label_pad) #y axis label
axs[0, 0].set_box_aspect(1) #  plot size
sns.despine(ax=axs[0, 0]) #  remove box outline
axs[0, 0].set_title('LHA dopamine', fontsize=8)
# 
# #  draw box on plot for cue
rect = patches.Rectangle((0, -0.5),
                         width=5,
                         height=3,
                         alpha=0.5,
                         facecolor=cue_color,
                         axes=axs[0, 0])
axs[0, 0].add_patch(rect)
# 
sns.lineplot(data=NAc_Cue_sucrose_df, #sucrose
             x='timestamps',
             y='mean',
             linewidth=0.4,
             color=sucrose_color,
             ax=axs[0, 1])
sns.lineplot(data=NAc_Cue_sucralose_df, #sucralose
             x='timestamps',
             y='mean',
             linewidth=0.4,
             color=sucralose_color,
             ax=axs[0, 1])

# #  fill error
axs[0, 1].fill_between(NAc_Cue_sucrose_df['timestamps'], #sucrose
                    (NAc_Cue_sucrose_df['mean']+NAc_Cue_sucrose_df['err']),
                    (NAc_Cue_sucrose_df['mean']-NAc_Cue_sucrose_df['err']),
                    color=sucrose_color,
                    alpha=0.3,
                    linewidth=0)
axs[0, 1].fill_between(NAc_Cue_sucralose_df['timestamps'], #sucralose
                    (NAc_Cue_sucralose_df['mean']+NAc_Cue_sucralose_df['err']),
                    (NAc_Cue_sucralose_df['mean']-NAc_Cue_sucralose_df['err']),
                    color=sucralose_color,
                    alpha=0.3,
                    linewidth=0)

axs[0, 1].set_xlim(left=-5, right=15) # x axis range
axs[0, 1].set_xticks([0,5,10])
axs[0, 1].set_ylim(bottom=-0.5, top=2.5)# y axis range
axs[0, 1].set_yticks([0,1,2])
axs[0, 1].tick_params(axis='both', which='major', labelsize=8) # set tick label size
axs[0, 1].set_xlabel('Time(sec)',fontsize = 8, labelpad=label_pad) #    x axis label
axs[0, 1].set_ylabel('z-score', fontsize = 8, labelpad=label_pad) #y axis label
axs[0, 1].set_box_aspect(1) #  plot size
sns.despine(ax=axs[0, 1]) #  remove box outline
axs[0, 1].set_title('NAc dopamine', fontsize=8)
# 
# #  draw box on plot for cue
rect = patches.Rectangle((0, -0.5),
                         width=5,
                         height=3,
                         alpha=0.5,
                         facecolor=cue_color,
                         axes=axs[0, 1])
axs[0, 1].add_patch(rect)


# #lineplot of lick frequency
sns.lineplot(ax=axs[0, 2],
             data = lick_freq_sucrose_df,
             x='time_sec',
             y='mean_smooth',
             color=sucrose_color,
             linewidth=0.4,
             legend=False)
sns.lineplot(ax=axs[0, 2],
             data = lick_freq_sucralose_df,
             x='time_sec',
             y='mean_smooth',
             color=sucralose_color,
             linewidth=0.4,
             legend=False)

axs[0, 2].fill_between(lick_freq_sucrose_df['time_sec'],
                    (lick_freq_sucrose_df['mean_smooth']+lick_freq_sucrose_df['sem_smooth']), #SEM
                    (lick_freq_sucrose_df['mean_smooth']-lick_freq_sucrose_df['sem_smooth']),#SEM
                    color=sucrose_color,
                    alpha=0.3,
                    linewidth=0)
axs[0, 2].fill_between(lick_freq_sucralose_df['time_sec'],
                    (lick_freq_sucralose_df['mean_smooth']+lick_freq_sucralose_df['sem_smooth']), #SEM
                    (lick_freq_sucralose_df['mean_smooth']-lick_freq_sucralose_df['sem_smooth']),#SEM
                    color=sucralose_color,
                    alpha=0.3,
                    linewidth=0)

# #remove spines
sns.despine(ax=axs[0, 2],
            top=True,
            right=True,
            offset=None,
            trim=False)
axs[0, 2].set_box_aspect(1)  # size of plot

axs[0, 2].set_xlim(left=-5, right=15)
axs[0, 2].set_xticks([0,5,10])
axs[0, 2].set_xlabel('Time(sec)', fontsize = 8, labelpad=label_pad)  # x axis label

axs[0, 2].set_ylim(bottom=-0.5, top=7)
axs[0, 2].set_yticks([0,3,6])
axs[0, 2].set_ylabel('licks/sec',  fontsize = 8, labelpad=label_pad) # y axis label

axs[0, 2].tick_params(axis='both', which='major', labelsize=8) # set tick label size



axs[0, 2].set_title('lick rate', fontsize = 8)
# #draw box on plot for cue
rect = patches.Rectangle((0,-0.5),
                         width=5,
                         height=7.5,
                         alpha=0.5,
                         facecolor=cue_color,
                         axes=axs[0, 2])
axs[0, 2].add_patch(rect)


sns.regplot(ax=axs[1,0],
            data = AUC_df,
            x='lick rate',
            y='LHA_Cue_AUC_E3',
            color = 'grey',
            # line_kws={},
            label="label",
            scatter=False)
sns.scatterplot(ax=axs[1, 0],
                data = AUC_df,
                x='lick rate',
                y='LHA_Cue_AUC_E3',
                size=3,
                alpha=0.75,
                hue='Treatment',
                palette=[sucrose_color, sucralose_color],
                legend=False)
axs[1, 0].set_box_aspect(1)

axs[1, 0].tick_params(axis='both', which='major', labelsize=8) # set tick label size

axs[1, 0].set_xlabel('licks/sec',fontsize = 8, labelpad=label_pad) #    x axis label

axs[1, 0].set_ylabel('dLight AUC(x10\u00b3)', fontsize = 8, labelpad=label_pad) #y axis label
axs[1, 0].set_ylim(bottom=-0.5, top=3) #  y axis range
axs[1, 0].set_yticks([0,1,2,3])#  y axis ticks
axs[1, 0].set_box_aspect(1) #  plot size
sns.despine(ax=axs[1, 0]) #  remove box outline
axs[1, 0].set_title('LHA dopamine vs \n anticipatory licks', fontsize=8)
axs[1, 0].text(0.5,2.5, 'r\u00b2='+str(LHA_R2) + '\np=' +str(LHA_pval), #  add r2 and p_value to plot
               fontsize=6,
               horizontalalignment='left',
               verticalalignment='center',
               color = sucrose_color)


sns.regplot(ax=axs[1,1],
            data = AUC_df,
            x='lick rate',
            y='NAC_Cue_AUC_E3',
            color = 'grey',
            # line_kws={},
            label="label",
            scatter=False)
sns.scatterplot(ax=axs[1, 1],
                data = AUC_df,
                x='lick rate',
                y='NAC_Cue_AUC_E3',
                hue='Treatment',
                size = 3,
                alpha=0.75,
                palette=[sucrose_color, sucralose_color],
                legend=False)

axs[1, 1].set_box_aspect(1)
axs[1, 1].tick_params(axis='both', which='major', labelsize=8) # set tick label size
axs[1, 1].set_xlabel('licks/sec',fontsize = 8, labelpad=label_pad) #    x axis label

axs[1, 1].set_ylabel('dLight AUC(x10\u00b3)', fontsize = 8, labelpad=label_pad) #y axis label
axs[1, 1].set_ylim(bottom=-0.5, top=6) #  y axis range
axs[1, 1].set_yticks([0,2,4,6,])#  y axis ticks
axs[1, 1].text(0.5,5.5, 'r\u00b2='+str(NAC_R2) + '\np=' +str(NAC_pval), #  add r2 and pvalue to plot
               fontsize=6,
               horizontalalignment='left',
               verticalalignment='center',
               color = sucrose_color)

sns.despine(ax=axs[1, 1]) #  remove box outline
axs[1, 1].set_title('NAC dopamine vs \n anticipatory licks', fontsize=8)

# LEGEND
axs[0, 0].text(-6,0.9, 'Sucrose',
            horizontalalignment='left',
            verticalalignment='center',
            color = sucrose_color)
axs[0, 0].text(-6,0.8, 'Sucralose',
            horizontalalignment='left',
            verticalalignment='center',
            color = sucralose_color)
axs[1, 2].set_box_aspect(1) #  plot size

##plt param and save
plt.tight_layout()
plt.rcParams['svg.fonttype'] = 'none' #save text as text in svg
plt.savefig(path_to_save + '\\sucrose_vs_sucralose_final_day.tiff',
            dpi=300,
            transparent=True)
plt.savefig(path_to_save + '\\sucrose_vs_sucralose_final_day.svg',
            dpi=300,
            transparent=True)
plt.show()





#%%

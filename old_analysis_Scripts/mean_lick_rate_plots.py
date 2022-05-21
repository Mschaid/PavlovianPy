
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import os
import glob

path_to_sucrose=(r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_training\day13\day13_csv_timestamps_analyzed_behavior_data\day13_lick_frequency.csv')
day = os.path.basename(path_to_sucrose).split('_')[0]
df_sucrose = pd.read_csv(path_to_sucrose)

path_to_sucralose=(r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\sucrose_to_sucralose\day3\day3_csv_timestamps_analyzed_behavior_data\day3_lick_frequency.csv')
day = os.path.basename(path_to_sucralose).split('_')[0]
df_sucralose = pd.read_csv(path_to_sucralose)

df_sucrose = (df_sucrose.iloc[:,:(df_sucrose.columns.get_loc('time_sec')+1)] #drop all columns after time_sec
              .drop(['mean','std'], axis=1) #drop mean and smooth column from stored data
               .melt('time_sec') #reform table around time
              .assign(treatment = 'sucrose',
                      day = day
                      ) #add group column for downstream grouping
              .rename(columns={"variable":"mouse", "value":"lick_rate",}) #rename columns
              )
df_sucralose = (df_sucralose.iloc[:,:(df_sucralose.columns.get_loc('time_sec')+1)] #drop all columns after time_sec
              .drop(['mean','std'], axis=1) #drop mean and smooth column from stored data
              .melt('time_sec') #reform table around time
              .assign(treatment = 'sucralose',
                      day = day
                      ) #add group column for downstream grouping
              .rename(columns={"variable":"mouse", "value":"lick_rate",}) #rename columns
              )
#%%

#   SUCROSE
base_lickfreq = (df_sucrose[df_sucrose['time_sec'].between(-5,0)]
                 .groupby(by=['mouse','treatment','day']).mean()
                 .assign(lick_category='baesline')
                 .reset_index())
ant_lickfreq = (df_sucrose[df_sucrose['time_sec'].between(0,5)]
                .groupby(by=['mouse','treatment','day'])
                .mean()
                .assign(lick_category='anticipatory')
                .reset_index())
rew_lickfreq = (df_sucrose[df_sucrose['time_sec'].between(5,10)]
                .groupby(by=['mouse','treatment', 'day'])
                .mean()
                .assign(lick_category='reward')
                .reset_index())
# SUCRALOSE
base_lickfreq_lose = (df_sucralose[df_sucralose['time_sec'].between(-5,0)]
                      .groupby(by=['mouse','treatment','day'])
                      .mean()
                      .assign(lick_category='baesline')
                      .reset_index())
ant_lickfreq_lose = (df_sucralose[df_sucralose['time_sec'].between(0,5)]
                     .groupby(by=['mouse','treatment','day'])
                     .mean()
                     .assign(lick_category='anticipatory')
                     .reset_index())
rew_lickfreq_lose = (df_sucralose[df_sucralose['time_sec'].between(5,10)]
                     .groupby(by=['mouse','treatment', 'day'])
                     .mean()
                     .assign(lick_category='reward')
                     .reset_index())

mean_lickfreq_df=pd.concat([base_lickfreq, ant_lickfreq, rew_lickfreq, base_lickfreq_lose, ant_lickfreq_lose, rew_lickfreq_lose]).reset_index()

print(mean_lickfreq_df)

#%%
data = (mean_lickfreq_df.groupby(by = ['treatment', 'lick_category'])
        .mean().
        reset_index()
        )
print(data)
mean_lickfreq_df.to_csv(r"R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\\mean_lick.csv", index = False, header=True)
#%%
colors = ['k', 'r']
colors_swarm = ['grey','grey']
sns.boxplot(data = mean_lickfreq_df, x='lick_category',
            y='lick_rate',
            hue= 'treatment',
            palette = colors
            # palette = 'muted'
               )
sns.swarmplot(data = mean_lickfreq_df, x='lick_category'
              , y='lick_rate',
              hue= 'treatment',
              dodge= True,
              palette=colors_swarm
               # palette = 'muted'
               )
plt.rcParams['svg.fonttype'] = 'none' #save text as text in svg
plt.savefig(r'C:\Users\mds8301\Desktop\FP_transfer'+ '\\_fig.tiff',
            dpi=300,
            transparent=True)
plt.show()

# rew_licks_df = df_sucrose.loc[(df_sucrose['time_sec'] >=5) & (df_sucrose['time_sec'] < 10)]

#%%
#  makes figure
fig, axs = plt.subplots(nrows=2,
                        ncols=2,
                        sharex=True,
                        squeeze=True,
                        figsize=(3, 3))  # sets # of plots columns x ros

fig.suptitle(day + 'sucralose\n post sucrose training', fontsize=12)  # figure title
fig.align_ylabels()

#  photometry plot for NAc cue
#  mean line and axs

plt.savefig(path_to_analyzed_data+'\\'+day+'_behavior_NAC_LHA_Cue.tiff',
            dpi=300,
            transparent=True)
plt.savefig(path_to_analyzed_data+'\\'+day+'_behavior_NAC_LHA_Cue.svg',
            dpi=300,
            transparent=True)
plt.show()





#%%


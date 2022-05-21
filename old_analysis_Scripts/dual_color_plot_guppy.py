
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import os
import glob



path_to_save = r'R:\Mike\Grants\NRSA F32\Figures'
path_to_gcamp=r'R:\Jillian\JS_for_MS\F336-210610-153852_output_1\CellTransients_axon_z_score_axon.h5'
path_to_dlight = r'R:\Jillian\JS_for_MS\F336-210610-153852_output_1\CellTransients_receptor_z_score_receptor.h5'


#  read photometry PSTH plots

gcamp_df = pd.read_hdf(path_to_gcamp)
gcamp_df = gcamp_df.iloc[::2,:].rolling(window=250, center = True).mean() # downsample and rolling average FP data
dlight_df = pd.read_hdf(path_to_dlight)
dlight_df = dlight_df.iloc[::2,:].rolling(window=250, center = True).mean()# downsample and rolling average FP data


#%%
#  makes figure
fig, axs = plt.subplots(
                        squeeze=True,
                        figsize=(2,2)
)  # sets # of plots columns x ros

# fig.suptitle(day, fontsize=12)  # figure title
# fig.align_ylabels()

#  photometry plot for NAc cue
#  mean line and axs
sns.lineplot(data=gcamp_df,
             x='timestamps',
             y='mean',
             linewidth=0.2,
             color='g',
             ax=axs)
sns.lineplot(data=dlight_df,
             x='timestamps',
             y='mean',
             linewidth=0.2,
             color='r',
             ax=axs)

#  fill error
axs.fill_between(gcamp_df['timestamps'],
                    (gcamp_df['mean']+gcamp_df['err']),
                    (gcamp_df['mean']-gcamp_df['err']),
                    color='g',
                    alpha=0.3,
                    linewidth=0)
axs.fill_between(dlight_df['timestamps'],
                 (dlight_df['mean']+dlight_df['err']),
                 (dlight_df['mean']-dlight_df['err']),
                 color='r',
                 alpha=0.3,
                 linewidth=0)

axs.tick_params(axis='both', which='major', labelsize=8) # set tick label size
axs.set_xlabel('Time(sec)',fontsize = 8) #    x axis label
axs.set_xlim(left=-5, right=10) #  x axis limit
axs.set_xticks([0,5,10]) #  x axis tick label
axs.set_xlabel('Time(sec)', fontsize = 8, labelpad=2)  # x axis label
axs.set_ylim(bottom=-.5, top=1.5) # y axis limit
axs.set_yticks([0,0.75, 1.5]) # y tick labels
axs.set_ylabel('z-score',  fontsize = 8, labelpad=2) # y axis label



sns.despine(ax=axs) #  remove box outline

plt.tight_layout()
plt.rcParams['svg.fonttype'] = 'none' #  save text as text in tiff
plt.savefig(path_to_save+'\\' + '_2_color.tiff',
            dpi=300,
            transparent=True)
plt.savefig(path_to_save+'\\' + '_2_color.svg', #  save text as text in svg
            dpi=300,
            transparent=True)
plt.show()



#%%


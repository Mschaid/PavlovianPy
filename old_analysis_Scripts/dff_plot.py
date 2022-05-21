import numpy as np
import pandas as pd
import h5py
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns

path_to_files =r'R:\Mike\Blood_Glucose_project\LH_NAC_Headfix\Photometry\Pav Training\cohort2\day12'
dff_folder = path_to_files + '\\' +path_to_files.split('\\')[-1] +'_csv_dff'
if not os.path.exists(dff_folder):
    os.mkdir(dff_folder)
    print("Directory created")
else:
    print("Directory already exists")
 # search path_to_files for all directories, then find subdirs that contain 'output' - append paths to list mouse_dirs
mouse_dirs = []
directories = os.listdir(path_to_files)
for dir in directories:
    path = os.path.join(path_to_files, dir, dir+'_output_*')
    output_path = glob.glob(path)
    mouse_dirs.append(output_path)

mouse_dirs = [element for element in mouse_dirs if element != []] ## drop empty elements from list
#%%
#  function to extract cue and lick timestamps
def get_dff(dir_path):
    path = ''.join([str(item) for item in dir_path]) # covert list index of path to pure string
    dff_LH_file= glob.glob(path + "/**/dff_LH.hdf5", recursive=True) #  search all directories for 'CCue.hdf5" file
    dff_LH_file = ''.join([str(item) for item in dff_LH_file]) # covert list index into pure string for 'CCue.hdf5" file
    dff_LH_h5 = h5py.File(dff_LH_file, 'r').get('data')# read timestamps from  'CCue.hdf5" file



    d = dict(dff = np.array(dff_LH_h5), #make dictioniary from cue and lick timestamps
            )
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in d.items()])) #covert dict into dataframe
    day = path.split('\\')[-3] # get day ID from path
    mouse_id =path.split('\\')[-1].split('_')[0] # get mouse ID from path
    df.to_csv(dff_folder+'\\'+ mouse_id+ '_'+ day+'_timestamps.csv') #save dataframe to csv in new_path
    print(mouse_id +' '+  day + ' ' + 'dff csv file saved')

#%%
for d in mouse_dirs: #apply function all directories in mouse_dirs
    get_dff(d)
print('all dff csv files saved')

#%%

grp_df =pd.DataFrame()
for f in os.scandir(dff_folder): #path is to folder containing aligned event csvs.
    mouse = mouse_id = os.path.basename(f).split('_')[0]
    df = pd.read_csv(f)
    grp_df[mouse]=df['dff']
grp_df = (grp_df.assign(mean=grp_df.mean(axis=1), #  add mean, standered dev and x-axis time to dataframe
                  std=grp_df.std(axis=1),
                  sem = grp_df.sem(axis =1))
          .rolling(window=1000, center = True).mean()
          .iloc[::10,:]
          .reset_index(level=0)
          .dropna()
          )
print(grp_df)
#%%
plt.plot(grp_df['index'], grp_df['mean'])

#%%

import os
import glob
import shutil
import pavlovian_functions as pv

path_to_files = r"C:\Users\mds8301\Desktop\FP_transfer\Day_2"
sub_dirs = pv.list_subdirs(path_to_files)

master_stores_list = r"R:\Mike\LHA_dopamine\LH_NAC_Headfix_FP\Photometry\Pav Training\2_color_pav\master_stores_list\storesList.csv"


for s in sub_dirs:
    basename = os.path.basename(s)
    pv.create_new_dir(s, f"{basename}_output_1")
output_dirs = glob.glob(path_to_files + "\**\*output_*")

for dir in output_dirs:
    shutil.copy(master_stores_list, dir)
#%%

files_to_remove = glob.glob(path_to_files + "\**\Pynapse1_call_log.csv*")

for f in files_to_remove:
    if os.path.exists(f):
        os.remove(f)
        print("file removed")
    else:
        print("file not found")

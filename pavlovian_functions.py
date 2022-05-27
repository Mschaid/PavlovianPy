import numpy as np
import pandas as pd
import h5py
import os
import glob


def create_new_dir(file_path, new_dir_ext):
    new_directory = os.path.join(file_path, new_dir_ext)
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)
        print('directory created')
    else:
        print('directroy already exists')


def find_ts_file_path(file_path, file_basename):
    for root, dirs, files in os.walk(file_path):
        if file_basename in files:
            return os.path.join(root, file_basename)


def read_timestamps(file_path):
    ts_arr = h5py.File(file_path, "r").get('ts')
    return np.array(ts_arr)


def list_subdirs(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory)]


def align_events(df, event, event_align):
    event_arr = df[event][np.where(df[event] != 0)[0]].dropna()
    event_align_arr = df[event_align].dropna().to_numpy()
    align_events_dict = {}
    for i in range(event_arr.shape[0]):
        arr = np.array(event_align_arr - event_arr[i])
        align_events_dict[i] = arr
        new_df = pd.DataFrame(dict([(k, pd.Series(v))
                              for k, v in align_events_dict.items()]))
    return new_df


def calc_frequency(filepath, low_time=-10, high_time=20, bins=155, convertion_factor=5):
    # time is in seconds
    df = pd.read_csv(filepath)  # read csv
    arr = df[(df > -low_time) & (df < high_time)].to_numpy()  #
    arr = arr[np.logical_not(np.isnan(arr))]
    freq = np.histogram(arr, bins=bins)[0] / len(df.columns)
    freq_convert = freq * convertion_factor
    return freq_convert


def flatten_df(df):
    df.columns = df.columns = ['_'.join(col) for col in df.columns.values]
    df = df.reset_index()
    return df

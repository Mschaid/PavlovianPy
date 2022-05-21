import os
import glob
import pandas as pd


path = r"C:\Users\mds8301\Desktop\FP_transfer\Day_1"
call_logs = glob.glob(path+"//**/*_call_log.csv")
ts_list=['Cue', 'Reward']

def clean_df(df): ## function to clean and organize dataframe
    df_clean = (df.rename(columns=lambda c: c.replace(" ", "_")) #  replace all space with _ in column names
                .rename(columns={"Start": "timestamps", "State_Name": "event"}) #  change column name "Start" to "timestamps"
                .pipe(lambda df: df[df.Call == 's_State_enter']) #  filter timestamps for when event initiates
            )
    return df_clean

def get_pynapse_timestamps(df, event): ## function to get timestamps of interest
    ts = df[df.event == event]['timestamps']
    return ts

for f in call_logs:
    for t in ts_list:
        df= (pd.read_csv(f)
             .pipe(clean_df)
             .pipe(lambda df: get_pynapse_timestamps(df, event= t))
             .to_csv(os.path.dirname(f)+f'//{t}.csv', index=False)
             )
    os.remove(f)
# print(df_test)



import beh_functions
from beh_functions import downsample_behavior
from beh_functions import process_behavior_reward
from beh_functions import import_csvs
from beh_functions import average_around_timestamp
from beh_functions import export_csvs

#input folder of behavior files
file_path = input("Please enter file path with behavior exports: ")

#Import necesary files as designated
dfs = import_csvs(file_path)
print('Data Imported')

#Downsample all files keeping the file name associated
downsampled_dfs = {}
for name, data in dfs.items():
    df_downsampled= downsample_behavior(data)
    downsampled_dfs[name] = df_downsampled
print('Behavior Data Downsampled!')

#Process all downsampled data keeping file name associated
processed_dfs={}
for name, data in downsampled_dfs.items():
    df_processed = process_behavior_reward(data)
    processed_dfs[name] = df_processed
print('Behavior Data Processed!')

#Analyze nosepoking timeseries data around cue light activity
averaged_data={}
for name, data in processed_dfs.items():
    df_averaged = average_around_timestamp(data,'CUE LIGHT ACTIVE','NOSE POKE ACTIVE')
    averaged_data[name] = df_averaged
print('Timeseries Analyzed!')

#Designate output folder path and export a single csv
export_path = input("Please enter file path for analysis export:")
filename = input("Please enter name of file to be exported for reward nosepoking timeseries data:")

export_csvs(averaged_data,filename,export_path)
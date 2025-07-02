import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import mount_speed

#input folder of behavior files
file_path = input("Please enter file path with raw behavior exports: ")

#Import necesary files as designated
dfs = import_csvs(file_path)
print('Data Imported')

#Downsample all files keeping the file name associated
downsampled_dfs = {}
for name, data in dfs.items():
    df_downsampled= downsample_behavior(data)
    downsampled_dfs[name] = df_downsampled
print('Behavior Data Downsampled!')

#Select necessary command file
command_df= (list(downsampled_dfs.values()))[2] #Creates a list of dataframes and then selects the 3rd one as command

#Process all downsampled data keeping file name associated
processed_dfs={}
for name, data in downsampled_dfs.items():
    df_processed = process_behavior(data, command_df=command_df)
    processed_dfs[name] = df_processed

#Continue with secondary processing to create columns for each presentation type
processed_var_dfs={}
for name, data in processed_dfs.items():
    df_var = overlap_beh_processing(data)
    processed_var_dfs[name] = df_var
print('Behavior Data Processed!')

FINISH THIS
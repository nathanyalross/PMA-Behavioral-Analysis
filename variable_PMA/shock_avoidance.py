import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import avoid_shock
from beh_functions import export_csvs

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
    df_processed = process_behavior(data, command_df=command_df, cues = ['NEW SPEAKER ACTIVE','CUE LIGHT ACTIVE'])
    processed_dfs[name] = df_processed
print('Behavior Data Processed!')

#Process shock avoidance data
shock_av = {}
for name, data in processed_dfs.items():
    shock_count = avoid_shock(data)
    shock_av[name]=shock_count
print('Shock Data Processed!')

export_path = input("Please enter file path for shock avoidance export:")
filename = input("Please enter name of file to be exported for shock avoidance data:")

export_csvs(shock_av, filename, export_path)
# Import modules to allow upstream integration of beh_functions file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import average_around_timestamp
from beh_functions import export_csvs
from beh_functions import meta_analysis

#Create lists for input dataframes and analysis that has been ran
input_titles = []
ran_analysis = []

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
    input_titles.append(name)
print('Behavior Data Downsampled!')

#OPTIONAL - Select command dataframe if all boxes don't get ttl signals.
#command_df= (list(downsampled_dfs.values()))[2] #Creates a list of dataframes and then selects the 3rd one as command

#OPTIONAL - If needed, set the names of your columns manually.
columns_of_interest=['TIME (S)', 'FREEZING', 'IN PLATFORM', 'R_NOSE POKE ACTIVE', 'L_NOSE POKE ACTIVE'
                                       'R_CUE LIGHT ACTIVE', 'L_CUE LIGHT ACTIVE', 'SPEED (M/S)',
                                        'SPEAKER CHANNEL 1 ACTIVE', 'SHOCKER ACTIVE']

#OPTIONAL: Create Dictionary of timestamps to be used for processing

#Process all downsampled data keeping file name associated
processed_dfs={}
for name, data in downsampled_dfs.items():
    df_processed = process_behavior(data, cues=['R_CUE LIGHT ACTIVE','L_CUE LIGHT ACTIVE'],columns_of_interest=columns_of_interest, cue_duration=15)
    processed_dfs[name] = df_processed
print('Behavior Data Processed!')

#Analyze nosepoking timeseries data around right cue light activation
averaged_data={}
for name, data in processed_dfs.items():
    df_averaged = average_around_timestamp(data,'R_NOSE POKE ACTIVE','R_CUE LIGHT ACTIVE', time_after=30)
    averaged_data[name] = df_averaged
print('Right cue light timeseries analyzed!')

ran_analysis.append('Nosepoke Timeseries Right Cue Light Active')

#Designate output folder path and export a single csv
export_path = input("Please enter file path for analysis export:")
filename = input("Please enter name of file to be exported for right cue light nosepoking timeseries data:")

export_csvs(averaged_data,filename,export_path)

#Analyze nosepoking timeseries data around left cue light activation
averaged_data={}
for name, data in processed_dfs.items():
    df_averaged = average_around_timestamp(data,'L_NOSE POKE ACTIVE','L_CUE LIGHT ACTIVE', time_after=30)
    averaged_data[name] = df_averaged
print('Left cue light timeseries analyzed!')

ran_analysis.append('Nosepoke Timeseries Left Cue Light Active')

#Designate output folder path and export a single csv
export_path = input("Please enter file path for analysis export:")
filename = input("Please enter name of file to be exported for left cue light nosepoking timeseries data:")

export_csvs(averaged_data,filename,export_path)

#Create/upadate meta_analysis file
meta_path = input('Please enter path for meta-analysis export')
meta_analysis(meta_path, input_titles, ran_analysis)
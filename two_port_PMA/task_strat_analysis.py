# Import modules to allow upstream integration of beh_functions file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import task_strat
from beh_functions import meta_analysis

#Create lists for input dataframes and analysis that has been ran
input_titles = []
ran_analysis = []

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
    df_processed = process_behavior(data, cues=['R_CUE LIGHT ACTIVE','L_CUE LIGHT ACTIVE', 'SPEAKER CHANNEL 1 ACTIVE'],columns_of_interest=columns_of_interest, cue_duration=15)
    processed_dfs[name] = df_processed
print('Behavior Data Processed!')

#Analyze task strategies for all mice during right cue light activation
strat_data={}
for name, data in processed_dfs.items():
    strat_list = task_strat(data,'R_CUE LIGHT ACTIVE')
    strat_data[name] = strat_list
print('Task Strategy analyzed for right cue light periods!')

#Initialize lists to store dictionary values for conversion to dataframe
mice=[]
strat_value=[]
plat_time=[]
np_time=[]

#Store dictionary values in lists 
for mouse, values in strat_data.items():
    mice.append(mouse)
    strat_value.append(values[0])
    plat_time.append(values[1])
    np_time.append(values[2])

#Create dataframe out of mount data
cs_pl_task_strat_df = pd.DataFrame({'Original CSV':mice,
                            'Task Strategy Score':strat_value,
                            'Total Platform Time (s)':plat_time,
                            'Total Nosepoke Time (s)':np_time})

#Designate output folder path for right cue light data and export a single csv
export_path = input("Please enter file path for task strategy right cue light data:")
filename = input("Please enter name of file to be exported for task strategy right cue light data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_pl_task_strat_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Right cue light task strategy data exported!')

ran_analysis.append('Right cue light Task Strategy')

#Analyze task strategies for all mice during left cue light activation
strat_data={}
for name, data in processed_dfs.items():
    strat_list = task_strat(data,'L_CUE LIGHT ACTIVE')
    strat_data[name] = strat_list
print('Task Strategy analyzed for left cue light periods!')

#Initialize lists to store dictionary values for conversion to dataframe
mice=[]
strat_value=[]
plat_time=[]
np_time=[]

#Store dictionary values in lists 
for mouse, values in strat_data.items():
    mice.append(mouse)
    strat_value.append(values[0])
    plat_time.append(values[1])
    np_time.append(values[2])

#Create dataframe out of mount data
cs_min_task_strat_df = pd.DataFrame({'Original CSV':mice,
                            'Task Strategy Score':strat_value,
                            'Total Platform Time (s)':plat_time,
                            'Total Nosepoke Time (s)':np_time})

#Designate output folder path for left cue light data and export a single csv
export_path = input("Please enter file path for task strategy left cue light data:")
filename = input("Please enter name of file to be exported for task strategy left cue light data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_min_task_strat_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Left cue light task strategy data exported!')

ran_analysis.append('Left cue light Task Strategy')

#Create/upadate meta_analysis file
meta_path = input('Please enter path for meta-analysis export: ')
meta_analysis(meta_path, input_titles, ran_analysis)
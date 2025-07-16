# Import modules to allow upstream integration of beh_functions file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import task_strat
from beh_functions import overlap_beh_processing

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

#OPTIONAL - Select command dataframe if all boxes don't get ttl signals.
#command_df= (list(downsampled_dfs.values()))[2] #Creates a list of dataframes and then selects the 3rd one as command

#OPTIONAL - If needed, set the names of your columns manually.
#columns_of_interest = []

#Process all downsampled data keeping file name associated
processed_dfs={}
for name, data in downsampled_dfs.items():
    df_processed = process_behavior(data, cues=['CUE LIGHT ACTIVE', 'NEW SPEAKER ACTIVE'])#, command_df=command_df) 
    processed_dfs[name] = df_processed

#Continue with secondary processing to create columns for each presentation type
processed_var_dfs={}
for name, data in processed_dfs.items():
    df_var = overlap_beh_processing(data)
    processed_var_dfs[name] = df_var
print('Behavior Data Processed!')

#Analyze task strategies for all mice during light only periods
strat_data={}
for name, data in processed_var_dfs.items():
    strat_list = task_strat(data,'LIGHT ONLY')
    strat_data[name] = strat_list
print('Task Strategy analyzed for light only periods!')

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
light_task_strat_df = pd.DataFrame({'Original CSV':mice,
                            'Task Strategy Score':strat_value,
                            'Total Platform Time (s)':plat_time,
                            'Total Nosepoke Time (s)':np_time})

#Designate output folder path and export a single csv
export_path = input("Please enter file path for task strategy light only data:")
filename = input("Please enter name of file to be exported for task strategy light only data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
light_task_strat_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Light only task strategy data exported!')

#Analyze task strategies for all mice during tone only periods
strat_data={}
for name, data in processed_var_dfs.items():
    strat_list = task_strat(data,'TONE ONLY')
    strat_data[name] = strat_list
print('Task Strategy analyzed for tone only periods!')

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
tone_task_strat_df = pd.DataFrame({'Original CSV':mice,
                            'Task Strategy Score':strat_value,
                            'Total Platform Time (s)':plat_time,
                            'Total Nosepoke Time (s)':np_time})

#Designate output folder path and export a single csv
export_path = input("Please enter file path for task strategy tone only data:")
filename = input("Please enter name of file to be exported for task strategy tone only data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
tone_task_strat_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Tone only task strategy data exported!')

#Analyze task strategies for all mice during copresentation periods
strat_data={}
for name, data in processed_var_dfs.items():
    strat_list = task_strat(data,'CO-PRESENTATION')
    strat_data[name] = strat_list
print('Task Strategy analyzed for copresentation periods!')

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
cop_task_strat_df = pd.DataFrame({'Original CSV':mice,
                            'Task Strategy Score':strat_value,
                            'Total Platform Time (s)':plat_time,
                            'Total Nosepoke Time (s)':np_time})

#Designate output folder path and export a single csv
export_path = input("Please enter file path for task strategy copresentation data:")
filename = input("Please enter name of file to be exported for task strategy copresentation data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cop_task_strat_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Copresentation task strategy data exported!')

#Analyze task strategies for all mice during light then tone periods
strat_data={}
for name, data in processed_var_dfs.items():
    strat_list = task_strat(data,'LIGHT THEN TONE')
    strat_data[name] = strat_list
print('Task Strategy analyzed for light then tone periods!')

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
ltt_task_strat_df = pd.DataFrame({'Original CSV':mice,
                            'Task Strategy Score':strat_value,
                            'Total Platform Time (s)':plat_time,
                            'Total Nosepoke Time (s)':np_time})

#Designate output folder path and export a single csv
export_path = input("Please enter file path for task strategy light then tone data:")
filename = input("Please enter name of file to be exported for task strategy light then tone data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
ltt_task_strat_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Light then tone task strategy data exported!')

#Analyze task strategies for all mice during tone then light periods
strat_data={}
for name, data in processed_var_dfs.items():
    strat_list = task_strat(data,'TONE THEN LIGHT')
    strat_data[name] = strat_list
print('Task Strategy analyzed for tone then light periods!')

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
ttl_task_strat_df = pd.DataFrame({'Original CSV':mice,
                            'Task Strategy Score':strat_value,
                            'Total Platform Time (s)':plat_time,
                            'Total Nosepoke Time (s)':np_time})

#Designate output folder path and export a single csv
export_path = input("Please enter file path for task strategy tone then light data:")
filename = input("Please enter name of file to be exported for task strategy tone then light data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
ttl_task_strat_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Tone then light task strategy data exported!')
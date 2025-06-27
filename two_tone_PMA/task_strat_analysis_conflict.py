import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import task_strat

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

#Process all downsampled data keeping file name associated
processed_dfs={}
for name, data in downsampled_dfs.items():
    df_processed = process_behavior(data)
    processed_dfs[name] = df_processed
print('Behavior Data Processed!')

#Analyze task strategies for all mice during the CS+
strat_data={}
for name, data in processed_dfs.items():
    strat_list = task_strat(data,'CS+')
    strat_data[name] = strat_list
print('Task Strategy analyzed for CS+ periods!')

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

#Designate output folder path for CS+ mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for task strategy CS+ data:")
filename = input("Please enter name of file to be exported for task strategy CS+ data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_pl_task_strat_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('CS+ task strategy data exported!')

#Analyze task strategies for all mice during the CS-
strat_data={}
for name, data in processed_dfs.items():
    strat_list = task_strat(data,'CS-')
    strat_data[name] = strat_list
print('Task Strategy analyzed for CS- periods!')

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

#Designate output folder path for CS- mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for task strategy CS- data:")
filename = input("Please enter name of file to be exported for task strategy CS- data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_min_task_strat_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('CS- task strategy data exported!')
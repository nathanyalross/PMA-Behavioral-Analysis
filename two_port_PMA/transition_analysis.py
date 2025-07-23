# Import modules to allow upstream integration of beh_functions file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import mount_speed
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

#Analyze speed around mounting activity during right cue light activation
mount_data={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'R_CUE LIGHT ACTIVE', end_time=15)
    mount_data[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for right cue light periods!')

ran_analysis.append('Mount entire right cue light')


#Initialize lists to store dictionary values for conversion to dataframe
mice=[]
num_mounts=[]
mount_speeds=[]

#Store dictionary values in lists 
for mouse, values in mount_data.items():
    mice.append(mouse)
    num_mounts.append(values[0])
    mount_speeds.append(values[1])

#Create dataframe out of mount data
cs_mount_df = pd.DataFrame({'Original CSV':mice,
                            'Number of mounts':num_mounts,
                            'Average Speed':mount_speeds})


#Additional Analysis to inspect the mount speed during time period before shock and during shock
#Analyze speed around mounting activity during right cue light for the first 25 seconds, before shock onset
mount_data_pre_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'R_CUE LIGHT ACTIVE', end_time=10)
    mount_data_pre_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for right cue light periods preceding shock onset!')

ran_analysis.append('Mount before right cue light shock onset')

#Initialize lists to store dictionary values for conversion to dataframe
mice=[]
num_mounts=[]
mount_speeds=[]

#Store dictionary values in lists 
for mouse, values in mount_data_pre_shock.items():
    mice.append(mouse)
    num_mounts.append(values[0])
    mount_speeds.append(values[1])

cs_mount_df['Number of Mounts Pre-Shock'] = num_mounts
cs_mount_df['Average speed pre-Shock'] = mount_speeds

#Analyze speed around mounting activity during right cue light for the last 5 seconds, during and just before shock onset
mount_data_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'R_CUE LIGHT ACTIVE', start_time=10, end_time=15)
    mount_data_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for right cue light periods during shock onset!')

ran_analysis.append('Mount during right cue light shock onset')

#Initialize lists to store dictionary values for conversion to dataframe
mice=[]
num_mounts=[]
mount_speeds=[]

#Store dictionary values in lists 
for mouse, values in mount_data_shock.items():
    mice.append(mouse)
    num_mounts.append(values[0])
    mount_speeds.append(values[1])

cs_mount_df['Number of Mounts Shock'] = num_mounts
cs_mount_df['Average speed Shock'] = mount_speeds


#Designate output folder path for right cue light mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for averaged right cue light mounting data:")
filename = input("Please enter name of file to be exported for averaged right cue light mounting data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_mount_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('right cue light mount data exported!')

#Analyze speed around mounting activity during left cue light activation
mount_data={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'L_CUE LIGHT ACTIVE', end_time=15)
    mount_data[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for left cue light periods!')

ran_analysis.append('Mount entire left cue light')


#Initialize lists to store dictionary values for conversion to dataframe
mice=[]
num_mounts=[]
mount_speeds=[]

#Store dictionary values in lists 
for mouse, values in mount_data.items():
    mice.append(mouse)
    num_mounts.append(values[0])
    mount_speeds.append(values[1])

#Create dataframe out of mount data
cs_mount_df = pd.DataFrame({'Original CSV':mice,
                            'Number of mounts':num_mounts,
                            'Average Speed':mount_speeds})


#Additional Analysis to inspect the mount speed during time period before shock and during shock
#Analyze speed around mounting activity during left cue light for the first 25 seconds, before shock onset
mount_data_pre_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'L_CUE LIGHT ACTIVE', end_time=10)
    mount_data_pre_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for left cue light periods preceding shock onset!')

ran_analysis.append('Mount before left cue light shock onset')

#Initialize lists to store dictionary values for conversion to dataframe
mice=[]
num_mounts=[]
mount_speeds=[]

#Store dictionary values in lists 
for mouse, values in mount_data_pre_shock.items():
    mice.append(mouse)
    num_mounts.append(values[0])
    mount_speeds.append(values[1])

cs_mount_df['Number of Mounts Pre-Shock'] = num_mounts
cs_mount_df['Average speed pre-Shock'] = mount_speeds

#Analyze speed around mounting activity during left cue light for the last 5 seconds, during and just before shock onset
mount_data_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'L_CUE LIGHT ACTIVE', start_time=10, end_time=15)
    mount_data_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for left cue light periods during shock onset!')

ran_analysis.append('Mount during left cue light shock onset')

#Initialize lists to store dictionary values for conversion to dataframe
mice=[]
num_mounts=[]
mount_speeds=[]

#Store dictionary values in lists 
for mouse, values in mount_data_shock.items():
    mice.append(mouse)
    num_mounts.append(values[0])
    mount_speeds.append(values[1])

cs_mount_df['Number of Mounts Shock'] = num_mounts
cs_mount_df['Average speed Shock'] = mount_speeds


#Designate output folder path for left cue light mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for averaged left cue light mounting data:")
filename = input("Please enter name of file to be exported for averaged left cue light mounting data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_mount_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('left cue light mount data exported!')
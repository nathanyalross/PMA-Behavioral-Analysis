# Import modules to allow upstream integration of beh_functions file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
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

#OPTIONAL - Select command dataframe if all boxes don't get ttl signals.
#command_df= (list(downsampled_dfs.values()))[2] #Creates a list of dataframes and then selects the 3rd one as command

#OPTIONAL - If needed, set the names of your columns manually.
#columns_of_interest = []

#Create Dictionary of timestamps to be used for processing
disc_cues=['CS+','CS-']
disc_cues_onset={}
disc_cues_onset['CS+'] = [300, 570, 750, 840, 1020, 1290, 1470, 1560, 1740, 2010, 
                2100, 2370, 2550, 2640, 2820, 3090, 3270, 3360, 3540, 3810]
disc_cues_onset['CS-'] = [390, 480, 660, 930, 1110, 1200, 1380, 1650, 1830, 1920, 
                2190, 2280, 2460, 2730, 2910, 3000, 3180, 3450, 3630, 3720]

#Process all downsampled data keeping file name associated
processed_dfs={}
for name, data in downsampled_dfs.items():
    df_processed = process_behavior(data, disc_cues, cue_onsets = disc_cues_onset)
    processed_dfs[name] = df_processed
print('Behavior Data Processed!')

#Analyze speed around mounting activity during CS+
mount_data={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'CS+')
    mount_data[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for CS+ periods!')

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
#Analyze speed around mounting activity during CS+ for the first 25 seconds, before shock onset
mount_data_pre_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'CS+', end_time=25)
    mount_data_pre_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for CS+ periods preceding shock onset!')

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

#Analyze speed around mounting activity during CS+ for the last 5 seconds, during and just before shock onset
mount_data_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'CS+', start_time=25)
    mount_data_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for CS+ periods during shock onset!')

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


#Designate output folder path for CS+ mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for averaged CS+ mounting data:")
filename = input("Please enter name of file to be exported for averaged CS+ mounting data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_mount_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('CS+ mount data exported!')

#Analyze speed around mounting activity during CS+
mount_data={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'CS-')
    mount_data[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for CS+ periods!')

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

#Additional Analysis to inspect the mount speed during time period before end of tone and at end of tone
#Analyze speed around mounting activity during CS- for the first 25 seconds, before what would be shock onset
mount_data_pre_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'CS-', end_time=25)
    mount_data_pre_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for CS- periods preceding shock onset!')

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

#Analyze speed around mounting activity during CS- for the last 5 seconds, during and just before shock onset
mount_data_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'CS-', start_time=25)
    mount_data_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for CS- periods preceding shock onset!')

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

#Designate output folder path for CS- mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for averaged CS- mounting data export:")
filename = input("Please enter name of file to be exported for averaged CS- mounting data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_mount_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('CS- mount data exported!')
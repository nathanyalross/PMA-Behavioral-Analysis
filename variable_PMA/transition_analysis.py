# Import modules to allow upstream integration of beh_functions file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import mount_speed
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
    df_processed = process_behavior(data, cues = ['NEW SPEAKER ACTIVE', 'CUE LIGHT ACTIVE'])#, command_df=command_df)
    processed_dfs[name] = df_processed

#Continue with secondary processing to create columns for each presentation type
processed_var_dfs={}
for name, data in processed_dfs.items():
    df_var = overlap_beh_processing(data)
    processed_var_dfs[name] = df_var
print('Behavior Data Processed!')

#Analyze speed around mounting activity during tone only Presentations
mount_data={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'TONE ONLY')
    mount_data[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for tone only periods!')

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


#Analyze speed around mounting activity during tone only for the first 25 seconds of the cue, before shock onset
mount_data_pre_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'TONE ONLY', end_time=25)
    mount_data_pre_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for tone only periods preceding shock onset!')

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

#Analyze speed around mounting activity during tone only for the last 5 seconds, during and just before shock onset
mount_data_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'TONE ONLY', start_time=25)
    mount_data_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for tone only periods during shock onset!')

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


#Designate output folder path for tone only mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for averaged tone only mounting data:")
filename = input("Please enter name of file to be exported for averaged tone only mounting data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_mount_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Tone only mount data exported!')



#Analyze speed around mounting activity during copresentations
mount_data={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'CO-PRESENTATION')
    mount_data[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for copresentation periods!')

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


#Analyze speed around mounting activity during copresentations for the first 25 seconds of the cue, before shock onset
mount_data_pre_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'CO-PRESENTATION', end_time=25)
    mount_data_pre_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for copresentation periods preceding shock onset!')

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

#Analyze speed around mounting activity during copresentations for the last 5 seconds, during and just before shock onset
mount_data_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'CO-PRESENTATION', start_time=25)
    mount_data_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for copresentation periods during shock onset!')

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


#Designate output folder path for copresentation mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for averaged copresentation mounting data:")
filename = input("Please enter name of file to be exported for averaged copresentation mounting data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_mount_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Copresentation mount data exported!')



#Analyze speed around mounting activity during tone then light Presentations
mount_data={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'TONE THEN LIGHT')
    mount_data[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for tone then light periods!')

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


#Analyze speed around mounting activity during tone then light for the first 25 seconds of the cue, before shock onset
mount_data_pre_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'TONE THEN LIGHT', end_time=25)
    mount_data_pre_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for tone then light periods preceding shock onset!')

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

#Analyze speed around mounting activity during tone then light for the last 5 seconds, during and just before shock onset
mount_data_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'TONE THEN LIGHT', start_time=25)
    mount_data_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for tone then light periods during shock onset!')

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


#Designate output folder path for tone then light mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for averaged tone then light mounting data:")
filename = input("Please enter name of file to be exported for averaged tone then light mounting data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_mount_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('tone then light mount data exported!')



#Analyze speed around mounting activity during light then tone Presentations
mount_data={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'LIGHT THEN TONE', start_time = 15)
    mount_data[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for light then tone periods!')

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


#Analyze speed around mounting activity during light then tone for the first 25 seconds of the cue, before shock onset
mount_data_pre_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'LIGHT THEN TONE', start_time = 15, end_time=40)
    mount_data_pre_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for light then tone periods preceding shock onset!')

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

#Analyze speed around mounting activity during light then tone for the last 5 seconds, during and just before shock onset
mount_data_shock={}
for name, data in processed_dfs.items():
    mount_count, mount_speed_av = mount_speed(data,'LIGHT THEN TONE', start_time=40)
    mount_data_shock[name] = [mount_count,mount_speed_av]
print('Average Mounting speed analyzed for light then tone periods during shock onset!')

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


#Designate output folder path for light then tone mounting speed timeseries data and export a single csv
export_path = input("Please enter file path for averaged light then tone mounting data:")
filename = input("Please enter name of file to be exported for averaged light then tone mounting data:")

export_dir = Path(export_path)
export_dir.mkdir(parents=True, exist_ok=True)
cs_mount_df.to_csv(export_dir/f"{filename}.csv", index=True)
print('Tone then light mount data exported!')
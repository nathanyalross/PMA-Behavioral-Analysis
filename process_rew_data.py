from beh_functions import downsample_behavior
from beh_functions import process_behavior
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

#Create a list out of all the downsampled dataframes to use for our command dataframe
ds_dfs=list(downsampled_dfs.values())
#Select command dataframe out of the list to use in our processing function
com_df=ds_dfs[2]

#Specify cues to be processed and timestamps for cues unspecified in AnyMaze File for data processing if needed
#cues=[]
#cue_onsets={}
#cue_onsets[]=[]
#cue_onsets[]=[]

for name, data in downsampled_dfs.items():
    df_processed = process_behavior(data,cues=['CUE LIGHT ACTIVE'])
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
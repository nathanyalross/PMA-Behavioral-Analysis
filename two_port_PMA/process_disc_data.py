# Import modules to allow upstream integration of beh_functions file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import average_around_timestamp
from beh_functions import export_csvs
from beh_functions import behavior_binning
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

if input('Analyze Nosepoke Timeseries data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze nosepoking timeseries data around right cue light activation
    averaged_data={}
    for name, data in processed_dfs.items():
        df_averaged = average_around_timestamp(data,'R_NOSE POKE ACTIVE','R_CUE LIGHT ACTIVE', time_after=30)
        averaged_data[name] = df_averaged
    print('Timeseries right cue light Nosepoke Data Analyzed!')

    #Designate output folder path for right cue light activation nosepoke timeseries and export a single csv
    export_path = input("Please enter file path for right cue light Nosepoke Timeseries export:")
    filename = input("Please enter name of file to be exported for right cue light nosepoking timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze nosepoking timeseries data around left cue light activation
    averaged_data={}
    for name, data in processed_dfs.items():
        df_averaged = average_around_timestamp(data, 'L_NOSE POKE ACTIVE', 'L_CUE LIGHT ACTIVE', time_after=30)
        averaged_data[name] = df_averaged
    print('Timeseries left cue light Nosepoke Data Analyzed!')

    #Designate output folder path for left cue light nosepoke timeseries and export a single csv
    export_path = input("Please enter file path for left cue light Nosepoke Timeseries export:")
    filename = input("Please enter name of file to be exported for left cue light nosepoking timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    ran_analysis.append('Nosepoke Timeseries both cue lights')

if input('Analyze Platform Timeseries during CS Presentation data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze platform timeseries data around right cue light activation
    averaged_data={}
    for name, data in processed_dfs.items():
        df_averaged = average_around_timestamp(data,'IN PLATFORM','R_CUE LIGHT ACTIVE', time_after=30)
        averaged_data[name] = df_averaged
    print('Timeseries right cue light Platform Data Analyzed!')

    #Designate output folder path for right cue light platform timeseries and export a single csv
    export_path = input("Please enter file path for right cue light Platform Timeseries export:")
    filename = input("Please enter name of file to be exported for right cue light platform timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze platform timeseries data around left cue light activation
    averaged_data={}
    for name, data in processed_dfs.items():
        df_averaged = average_around_timestamp(data,'IN PLATFORM','L_CUE LIGHT ACTIVE', time_after=30)
        averaged_data[name] = df_averaged
    print('Timeseries left cue light Platform Data Analyzed!')

    #Designate output folder path for left cue light platform timeseries and export a single csv
    export_path = input("Please enter file path for left cue light platform Timeseries export:")
    filename = input("Please enter name of file to be exported for left cue light platform timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    ran_analysis.append('Platform Timeseries both cue lights')

if input('Analyze Nosepoke Histogram during CS Presentation data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze nosepoke histogram data around right cue light copresentation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'R_NOSE POKE ACTIVE','R_CUE LIGHT ACTIVE', bin_size=15)
        binned_data[name] = df_binned
    print('Histogram right cue light Nosepoke Data Analyzed!')

    #Designate output folder path for right cue light nosepoke histogram and export a single csv
    export_path = input("Please enter file path for right cue light Nosepoke Histogram export:")
    filename = input("Please enter name of file to be exported for right cue light nosepoke histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze nosepoke histogram data around left cue light activation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'L_NOSE POKE ACTIVE', 'L_CUE LIGHT ACTIVE', bin_size=15)
        binned_data[name] = df_binned
    print('Histogram left cue light Nosepoke Data Analyzed!')

    #Designate output folder path for left cue light nosepoke histogram and export a single csv
    export_path = input("Please enter file path for left cue light Nosepoke Histogram export:")
    filename = input("Please enter name of file to be exported for left cue light Nosepoke histogram data:")

    export_csvs(binned_data,filename,export_path)

    ran_analysis.append('Nosepoke Histogram both cue lights')

if input('Analyze Platform Histogram during CS Presentation data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze platform histogram data around right cue light activation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'IN PLATFORM','R_CUE LIGHT ACTIVE', bin_size=15)
        binned_data[name] = df_binned
    print('Histogram right cue light Platform Data Analyzed!')

    #Designate output folder path for right cue light platform histogram and export a single csv
    export_path = input("Please enter file path for right cue light NosepokPlatforme Histogram export:")
    filename = input("Please enter name of file to be exported for right cue light Platform histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze platform histogram data around left cue light activation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'IN PLATFORM','L_CUE LIGHT ACTIVE', bin_size=15)
        binned_data[name] = df_binned
    print('Histogram left cue light Platform Data Analyzed!')

    #Designate output folder path for left cue light platform histogram and export a single csv
    export_path = input("Please enter file path for left cue light Platform Histogram export:")
    filename = input("Please enter name of file to be exported for left cue light Platform histogram data:")

    export_csvs(binned_data,filename,export_path)

    ran_analysis.append('Platform Histogram both cue lights')

#Create/upadate meta_analysis file
meta_path = input('Please enter path for meta-analysis export: ')
meta_analysis(meta_path, input_titles, ran_analysis)
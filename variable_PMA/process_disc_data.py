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
    df_processed = process_behavior(data)#, command_df=command_df) 
    processed_dfs[name] = df_processed

#Continue with secondary processing to create columns for each presentation type
processed_var_dfs={}
for name, data in processed_dfs.items():
    df_var = overlap_beh_processing(data)
    processed_var_dfs[name] = df_var
print('Behavior Data Processed!')

#Analyze nosepoke timeseries data around different presentation types
if input('Analyze Nosepoke Timeseries data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze nosepoking timeseries data around light only presentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'NOSE POKE ACTIVE','LIGHT ONLY')
        averaged_data[name] = df_averaged
    print('Timeseries Light Only Nosepoke Data Analyzed!')

    #Designate output folder path for light only nosepoke timeseries and export a single csv
    export_path = input("Please enter file path for Light Only Nosepoke Timeseries export:")
    filename = input("Please enter name of file to be exported for light only nosepoking timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze nosepoking timeseries data around tone only presentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'NOSE POKE ACTIVE','TONE ONLY')
        averaged_data[name] = df_averaged
    print('Timeseries Tone Only Nosepoke Data Analyzed!')

    #Designate output folder path for tone only nosepoke timeseries and export a single csv
    export_path = input("Please enter file path for Tone Only Nosepoke Timeseries export:")
    filename = input("Please enter name of file to be exported for tone only nosepoking timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze nosepoking timeseries data around copresentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'NOSE POKE ACTIVE','CO-PRESENTATION')
        averaged_data[name] = df_averaged
    print('Timeseries Copresentation Nosepoke Data Analyzed!')

    #Designate output folder path for copresentation nosepoke timeseries and export a single csv
    export_path = input("Please enter file path for Copresentation Nosepoke Timeseries export:")
    filename = input("Please enter name of file to be exported for copresentation nosepoking timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze nosepoking timeseries data around light then tone copresentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'NOSE POKE ACTIVE','LIGHT THEN TONE', time_after = 60)
        averaged_data[name] = df_averaged
    print('Timeseries light then tone Nosepoke Data Analyzed!')

    #Designate output folder path for light then tone nosepoke timeseries and export a single csv
    export_path = input("Please enter file path for light then tone Nosepoke Timeseries export:")
    filename = input("Please enter name of file to be exported for light then tone nosepoking timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze nosepoking timeseries data around tone then light copresentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'NOSE POKE ACTIVE','TONE THEN LIGHT', time_after = 60)
        averaged_data[name] = df_averaged
    print('Timeseries tone then light Nosepoke Data Analyzed!')

    #Designate output folder path for tone then light timeseries and export a single csv
    export_path = input("Please enter file path for tone then light Nosepoke Timeseries export:")
    filename = input("Please enter name of file to be exported for tone then light nosepoking timeseries data:")

    export_csvs(averaged_data,filename,export_path)

#Analyze platform timeseries data around different presentation types
if input('Analyze Platform Timeseries data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze platform timeseries data around light only presentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'IN PLATFORM','LIGHT ONLY')
        averaged_data[name] = df_averaged
    print('Timeseries Light Only Platform Data Analyzed!')

    #Designate output folder path for light only platform timeseries and export a single csv
    export_path = input("Please enter file path for Light Only Platform Timeseries export:")
    filename = input("Please enter name of file to be exported for light only platform timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze platform timeseries data around tone only presentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'IN PLATFORM','TONE ONLY')
        averaged_data[name] = df_averaged
    print('Timeseries Tone Only Platform Data Analyzed!')

    #Designate output folder path for tone only platform timeseries and export a single csv
    export_path = input("Please enter file path for Tone Only Platform Timeseries export:")
    filename = input("Please enter name of file to be exported for tone only platform timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze platform timeseries data around copresentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'IN PLATFORM','CO-PRESENTATION')
        averaged_data[name] = df_averaged
    print('Timeseries Copresentation Platform Data Analyzed!')

    #Designate output folder path for copresentation platform timeseries and export a single csv
    export_path = input("Please enter file path for Copresentation Platform Timeseries export:")
    filename = input("Please enter name of file to be exported for copresentation platform timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze platform timeseries data around light then tone copresentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'IN PLATFORM','LIGHT THEN TONE', time_after = 60)
        averaged_data[name] = df_averaged
    print('Timeseries light then tone Platform Data Analyzed!')

    #Designate output folder path for light then tone platform timeseries and export a single csv
    export_path = input("Please enter file path for light then tone Platform Timeseries export:")
    filename = input("Please enter name of file to be exported for light then tone platform timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze platform timeseries data around tone then light copresentations
    averaged_data={}
    for name, data in processed_var_dfs.items():
        df_averaged = average_around_timestamp(data,'IN PLATFORM','TONE THEN LIGHT', time_after = 60)
        averaged_data[name] = df_averaged
    print('Timeseries tone then light Platform Data Analyzed!')

    #Designate output folder path for tone then light platform timeseries and export a single csv
    export_path = input("Please enter file path for tone then light Platform Timeseries export:")
    filename = input("Please enter name of file to be exported for tone then light platform timeseries data:")

    export_csvs(averaged_data,filename,export_path)

if input('Analyze Nosepoke Histogram data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze nosepoke histogram data around light only presentations
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'NOSE POKE ACTIVE','LIGHT ONLY')
        binned_data[name] = df_binned
    print('Histogram Light Only Nosepoke Data Analyzed!')

    #Designate output folder path for light only nosepoke histogram and export a single csv
    export_path = input("Please enter file path for Light Only Nosepoke Histogram export:")
    filename = input("Please enter name of file to be exported for light only nosepoke histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze nosepoke histogram data around tone only copresentation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'NOSE POKE ACTIVE','TONE ONLY')
        binned_data[name] = df_binned
    print('Histogram Tone Only Nosepoke Data Analyzed!')

    #Designate output folder path for tone only nosepoke histogram and export a single csv
    export_path = input("Please enter file path for Tone Only Nosepoke Histogram export:")
    filename = input("Please enter name of file to be exported for tone only nosepoke histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze nosepoke histogram data around copresentations
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'NOSE POKE ACTIVE','CO-PRESENTATION')
        binned_data[name] = df_binned
    print('Histogram Copresentation Nosepoke Data Analyzed!')

    #Designate output folder path for copresentation nosepoke histogram and export a single csv
    export_path = input("Please enter file path for Copresentation Nosepoke Histogram export:")
    filename = input("Please enter name of file to be exported for copresentation nosepoke histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze nosepoke histogram data around light then tone presentations
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'NOSE POKE ACTIVE','LIGHT THEN TONE', bin_size = 45)
        binned_data[name] = df_binned
    print('Histogram light then tone Nosepoke Data Analyzed!')

    #Designate output folder path for light then tone nosepoke histogram and export a single csv
    export_path = input("Please enter file path for light then tone Nosepoke Histogram export:")
    filename = input("Please enter name of file to be exported for light then tone nosepoke histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze nosepoke histogram data around tone then light presentations
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'NOSE POKE ACTIVE','TONE THEN LIGHT', bin_size = 45)
        binned_data[name] = df_binned
    print('Histogram tone then light Nosepoke Data Analyzed!')

    #Designate output folder path for tone then light nosepoke histogram and export a single csv
    export_path = input("Please enter file path for tone then light Nosepoke Histogram export:")
    filename = input("Please enter name of file to be exported for tone then light nosepoke histogram data:")

    export_csvs(binned_data,filename,export_path)

if input('Analyze Platform Histogram data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze platform histogram data around light only presentations
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'IN PLATFORM','LIGHT ONLY')
        binned_data[name] = df_binned
    print('Histogram Light Only Platform Data Analyzed!')

    #Designate output folder path for light only platform histogram and export a single csv
    export_path = input("Please enter file path for Light Only Platform Histogram export:")
    filename = input("Please enter name of file to be exported for light only platform histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze platform histogram data around tone only copresentation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'IN PLATFORM','TONE ONLY')
        binned_data[name] = df_binned
    print('Histogram Tone Only Platform Data Analyzed!')

    #Designate output folder path for tone only platform histogram and export a single csv
    export_path = input("Please enter file path for Tone Only Platform Histogram export:")
    filename = input("Please enter name of file to be exported for tone only platform histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze platform histogram data around copresentations
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'IN PLATFORM','CO-PRESENTATION')
        binned_data[name] = df_binned
    print('Histogram Copresentation Platform Data Analyzed!')

    #Designate output folder path for copresentation platform histogram and export a single csv
    export_path = input("Please enter file path for Copresentation Platform Histogram export:")
    filename = input("Please enter name of file to be exported for copresentation platform histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze platform histogram data around light then tone presentations
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'IN PLATFORM','LIGHT THEN TONE', bin_size = 45)
        binned_data[name] = df_binned
    print('Histogram light then tone Platform Data Analyzed!')

    #Designate output folder path for light then tone platform histogram and export a single csv
    export_path = input("Please enter file path for light then tone Platform Histogram export:")
    filename = input("Please enter name of file to be exported for light then tone platform histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze platform histogram data around tone then light presentations
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'IN PLATFORM','TONE THEN LIGHT', bin_size = 45)
        binned_data[name] = df_binned
    print('Histogram tone then light Platform Data Analyzed!')

    #Designate output folder path for tone then light platform histogram and export a single csv
    export_path = input("Please enter file path for tone then light Platform Histogram export:")
    filename = input("Please enter name of file to be exported for tone then light platform histogram data:")

    export_csvs(binned_data,filename,export_path)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import average_around_timestamp
from beh_functions import export_csvs
from beh_functions import behavior_binning

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
    df_processed = process_behavior(data, cue_onsets = disc_cues_onset, cues=disc_cues)
    processed_dfs[name] = df_processed
print('Behavior Data Processed!')

if input('Analyze Nosepoke Timeseries during CS Presentation data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze nosepoking timeseries data around CS+ copresentation
    averaged_data={}
    for name, data in processed_dfs.items():
        df_averaged = average_around_timestamp(data,'CS+','NOSE POKE ACTIVE')
        averaged_data[name] = df_averaged
    print('Timeseries CS+ Nosepoke Data Analyzed!')

    #Designate output folder path for CS+ nosepoke timeseries and export a single csv
    export_path = input("Please enter file path for CS+ Nosepoke Timeseries export:")
    filename = input("Please enter name of file to be exported for CS+ nosepoking timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze nosepoking timeseries data around CS- copresentation
    averaged_data={}
    for name, data in processed_dfs.items():
        df_averaged = average_around_timestamp(data,'CS-','NOSE POKE ACTIVE')
        averaged_data[name] = df_averaged
    print('Timeseries CS- Nosepoke Data Analyzed!')

    #Designate output folder path for CS- nosepoke timeseries and export a single csv
    export_path = input("Please enter file path for CS- Nosepoke Timeseries export:")
    filename = input("Please enter name of file to be exported for CS- nosepoking timeseries data:")

    export_csvs(averaged_data,filename,export_path)

if input('Analyze Platform Timeseries during CS Presentation data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze platform timeseries data around CS+ copresentation
    averaged_data={}
    for name, data in processed_dfs.items():
        df_averaged = average_around_timestamp(data,'CS+','IN PLATFORM')
        averaged_data[name] = df_averaged
    print('Timeseries CS+ Platform Data Analyzed!')

    #Designate output folder path for CS+ platform timeseries and export a single csv
    export_path = input("Please enter file path for CS+ Platform Timeseries export:")
    filename = input("Please enter name of file to be exported for CS+ platform timeseries data:")

    export_csvs(averaged_data,filename,export_path)

    #Analyze platform timeseries data around CS- copresentation
    averaged_data={}
    for name, data in processed_dfs.items():
        df_averaged = average_around_timestamp(data,'CS-','IN PLATFORM')
        averaged_data[name] = df_averaged
    print('Timeseries CS- Platform Data Analyzed!')

    #Designate output folder path for CS- platform timeseries and export a single csv
    export_path = input("Please enter file path for CS- platform Timeseries export:")
    filename = input("Please enter name of file to be exported for CS- platform timeseries data:")

    export_csvs(averaged_data,filename,export_path)

if input('Analyze Nosepoke Histogram during CS Presentation data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze nosepoke histogram data around CS+ copresentation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'NOSE POKE ACTIVE','CS+')
        binned_data[name] = df_binned
    print('Histogram CS+ Nosepoke Data Analyzed!')

    #Designate output folder path for CS+ nosepoke histogram and export a single csv
    export_path = input("Please enter file path for CS+ Nosepoke Histogram export:")
    filename = input("Please enter name of file to be exported for CS+ nosepoke histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze nosepoke histogram data around CS- copresentation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'NOSE POKE ACTIVE','CS-')
        binned_data[name] = df_binned
    print('Histogram CS- Nosepoke Data Analyzed!')

    #Designate output folder path for CS- nosepoke histogram and export a single csv
    export_path = input("Please enter file path for CS- Nosepoke Histogram export:")
    filename = input("Please enter name of file to be exported for CS- Nosepoke histogram data:")

    export_csvs(binned_data,filename,export_path)

if input('Analyze Platform Histogram during CS Presentation data? please respond with Y for yes or N for no: ') in ('Y', 'y'):
    #Analyze platform histogram data around CS+ copresentation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'IN PLATFORM','CS+')
        binned_data[name] = df_binned
    print('Histogram CS+ Platform Data Analyzed!')

    #Designate output folder path for CS+ platform histogram and export a single csv
    export_path = input("Please enter file path for CS+ NosepokPlatforme Histogram export:")
    filename = input("Please enter name of file to be exported for CS+ Platform histogram data:")

    export_csvs(binned_data,filename,export_path)

    #Analyze platform histogram data around CS- copresentation
    binned_data={}
    for name, data in processed_dfs.items():
        df_binned = behavior_binning(data,'IN PLATFORM','CS-')
        binned_data[name] = df_binned
    print('Histogram CS- Platform Data Analyzed!')

    #Designate output folder path for CS- platform histogram and export a single csv
    export_path = input("Please enter file path for CS- Platform Histogram export:")
    filename = input("Please enter name of file to be exported for CS- Platform histogram data:")

    export_csvs(binned_data,filename,export_path)
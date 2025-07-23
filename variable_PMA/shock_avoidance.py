# Import modules to allow upstream integration of beh_functions file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from beh_functions import downsample_behavior
from beh_functions import process_behavior
from beh_functions import import_csvs
from beh_functions import avoid_shock
from beh_functions import export_csvs
from beh_functions import meta_analysis
from beh_functions import overlap_beh_processing

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
#columns_of_interest = []

#Process all downsampled data keeping file name associated
processed_dfs={}
for name, data in downsampled_dfs.items():
    df_processed = process_behavior(data, cues = ['NEW SPEAKER ACTIVE','CUE LIGHT ACTIVE'])#, command_df=command_df)
    processed_dfs[name] = df_processed

#Continue with secondary processing to create columns for each presentation type
processed_var_dfs={}
for name, data in processed_dfs.items():
    df_var = overlap_beh_processing(data)
    processed_var_dfs[name] = df_var
print('Behavior Data Processed!')

#Process shock avoidance data for all presentations
shock_av = {}
for name, data in processed_dfs.items():
    shock_count = avoid_shock(data)
    shock_av[name]=shock_count
print('Shock Data Processed!')

ran_analysis.append('Shock Avoidance Analysis')

export_path = input("Please enter file path for shock avoidance export:")
filename = input("Please enter name of file to be exported for shock avoidance data:")

export_csvs(shock_av, filename, export_path)

if input('Process shock avoidance data for individual cue types? Please respond with Y for yes or N for no: ') in ('Y','y'):
     #Process shock avoidance data for tone only presentations
    shock_av = {}
    for name, data in processed_dfs.items():
        shock_count = avoid_shock(data, 'TONE ONLY')
        shock_av[name]=shock_count
    print('Tone Only Shock Data Processed!')

    ran_analysis.append('Tone only Shock Avoidance Analysis')

    export_path = input("Please enter file path for tone only shock avoidance export:")
    filename = input("Please enter name of file to be exported for tone only shock avoidance data:")

     #Process shock avoidance data for copresentations
    shock_av = {}
    for name, data in processed_dfs.items():
        shock_count = avoid_shock(data, 'CO-PRESENTATION')
        shock_av[name]=shock_count
    print('Copresentation Shock Data Processed!')

    ran_analysis.append('Copresentation Shock Avoidance Analysis')

    export_path = input("Please enter file path for copresentation shock avoidance export:")
    filename = input("Please enter name of file to be exported for copresentation shock avoidance data:")

     #Process shock avoidance data for light then tone
    shock_av = {}
    for name, data in processed_dfs.items():
        shock_count = avoid_shock(data, 'LIGHT THEN TONE')
        shock_av[name]=shock_count
    print('Light then Tone Shock Data Processed!')

    ran_analysis.append('LTT Shock Avoidance Analysis')

    export_path = input("Please enter file path for light then tone shock avoidance export:")
    filename = input("Please enter name of file to be exported for light then tone shock avoidance data:")

     #Process shock avoidance data for tone then light
    shock_av = {}
    for name, data in processed_dfs.items():
        shock_count = avoid_shock(data, 'TONE THEN LIGHT')
        shock_av[name]=shock_count
    print('Tone then Light Shock Data Processed!')

    ran_analysis.append('TTL Shock Avoidance Analysis')

    export_path = input("Please enter file path for tone then light shock avoidance export:")
    filename = input("Please enter name of file to be exported for tone then light shock avoidance data:")

#Create/upadate meta_analysis file
meta_path = input('Please enter path for meta-analysis export: ')
meta_analysis(meta_path, input_titles, ran_analysis)
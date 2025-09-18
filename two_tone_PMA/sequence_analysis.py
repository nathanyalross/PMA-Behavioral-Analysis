#Script that identifies sequences of activity from, in this case, a fed in ground truth, to then identify sequences and calculate
#Sole purpose of protocol is to define order of presentations

#Now: Write from scratch, goal is to take sequences and average values for the second pres in the sequence
#Export is CSV where mouse protocol names are on the columns, transition type on the rows, and values are the averaged data
#Input is behavior files? I suppose that would work

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

# Import modules to allow upstream integration of beh_functions file
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from beh_functions import calculate_auc
from beh_functions import import_csvs
from beh_functions import export_csvs

file_path = input("Please enter file path with processed timeseries data: ")

#Import necesary files as designated
dfs = import_csvs(file_path, 'timeseries')
print('Data imported')

#Calculate AUCs for timeseries data
auc_data={}
for name, data in dfs.items():
    df_auc = calculate_auc(data)
    auc_data[name] = df_auc
print('AUC data calculated!')

#Designate output folder path for CS+ nosepoke timeseries and export a single csv
export_path = input("Please enter file path for AUC data export:")
filename = input("Please enter name of file to be exported for AUC data:")

export_csvs(auc_data,filename,export_path)
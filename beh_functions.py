import pandas as pd 
import numpy as np
from pathlib import Path
from numpy import trapezoid

#The following function will downsample behavior data to appropriate frequency
def downsample_behavior(df, frequency_seconds=0.5):
    """
    Downsample by grouping data into time bins and averaging
    
    Args:
    df : The dataframe of behavior to be downsampled
    frequency_seconds : desired sampling frequency in seconds
    """
    
    # Prepare the dataframe
    df = df.copy()
    df = df.rename(columns={df.columns[0]: 'Time (s)'})
    df['Time (s)'] = pd.to_numeric(df['Time (s)'], errors='coerce')
    df = df.dropna(subset=['Time (s)']).reset_index(drop=True)
    
    # Create time bins
    min_time = df['Time (s)'].min()
    max_time = df['Time (s)'].max()
    time_bins = pd.cut(df['Time (s)'], 
                      bins=int((max_time - min_time) / frequency_seconds),
                      include_lowest=True)
    
    # Group by time bins and take mean
    df_downsampled = df.groupby(time_bins, observed=True).mean().reset_index(drop=True)
    
    # Create new time column with bin centers
    df_downsampled['Time (s)'] = df_downsampled.index * frequency_seconds + min_time
    
    print(f"Original: {len(df)} rows, Downsampled: {len(df_downsampled)} rows")
    return df_downsampled

#The following function will keep only necessary behavior information and create new information for reward training days
def process_behavior(df, 
                    columns_of_interest=['TIME (S)', 'FREEZING', 'IN PLATFORM', 'NOSE POKE ACTIVE',
                                       'CUE LIGHT ACTIVE', 'SPEED (M/S)', 
                                       'FEEDER ACTIVE', 'NEW SPEAKER ACTIVE', 'NEW SHOCKER ACTIVE'],
                    command_df = None,
                    cue_onsets = None,
                    cues=['NONE GIVEN'],
                    cue_duration = 30):
    """
    Args:
    df : downsampled behavior dataframe
    columns_of_interest: columns to keep from original behavior dataframe
    cue_onsets: Optional dictionary of nsets matched with necessary cue to manually create columns.
        Ideally this will be unneeded.  
    cues: list of task cues as strings to produce in resulting dataframe. For reward stage this is usually just when the cue light is active,
        but could be more than one in the case of two-port PMA, for example. 
        If no cues need to be fixed or added, leave as default.
    cue_duration: duration of cue periods in seconds (default 30)
    """

    df_downsampled = df.copy()

    df_downsampled.columns = df_downsampled.columns.str.upper()

    df_subset = df_downsampled[columns_of_interest].copy()

    #Set time as the index
    df_subset.set_index('TIME (S)', inplace=True)

    #Use the dataframe that receives anymaze outputs to create timestamps if one is given
    if command_df is not None:
        #Capitalize the column names in the command dataframe and create a copy
        command_df_proc=command_df.copy()
        command_df_proc.columns = command_df_proc.columns.str.upper()
        #Set time as index for proper alignment and processing
        command_df_proc.set_index('TIME (S)', inplace=True)
        #Iterate through each cue in list of cues 
        for cue in cues:
            #If the cue is in the command dataframe then copy over that column data
            if cue in command_df_proc:
                #Initialize the column for the cue
                df_subset[cue] = 0
                #Set the values for the cue column equal to the command file so they all match
                df_subset[cue] = command_df_proc[cue]
            #If the cue is not in command dataframe then use the given timestamps to create necessary df
            else:
                #Notify user that this column is being created manually
                print(f'Task phase {cue} not in command dataframe, using timestamps to create')
                try:
                    df_subset[cue] = 0
                    for onset in cue_onsets[cue]:
                        df_subset.loc[onset:onset+cue_duration, cue] = 1
                except:
                    print(f'Warning! No timestamps given for {cue}, please correct command dataframe or give timestamps.')
    else:
        for cue in cues:
            #If the cue list is left blank it can be assumed that all dataframes already have appropriate cues, no cue processing done
            if cue == 'NONE GIVEN':
                break
            else:
                print(f'Using timestamps to create task phase {cue}')
                if cue_onsets and cue in cue_onsets:  # null check
                    df_subset[cue] = 0
                    for onset in cue_onsets[cue]:
                        df_subset.loc[onset:onset+cue_duration, cue] = 1
                else:
                    print(f'Warning! No timestamps given for {cue}, please give timestamps.')
    
    #Create ITI columns using newly added task cue data
    #Initialize lists to collect off of the onset and offset timestamps
    iti_onsets_all = []
    iti_offsets_all = []

    #Initialize ITI column with 0's
    df_subset['ITI'] = 0

    #Iterate through the cues, finding the offsets and onsets to use for ITI onsets and offsets
    for cue in cues:
        #Specify offset as when the cue column ends
        offset_mask = (df_subset[cue] == 0) & (df_subset[cue].diff() < 0)
        iti_onsets = df_subset[offset_mask].index
        #Append the offset to list of offsets
        iti_onsets_all.extend(iti_onsets)

        #Specify onset as index before cue column begines
        onset_mask = (df_subset[cue] > 0) & (df_subset[cue].diff() > 0)
        #Identify indices where cue onset occurs
        mask_indices = df_subset[onset_mask].index
        iti_offsets = []
        #File through selected indices and take the value just before it
        for idx in mask_indices:
            pos = df_subset.index.get_loc(idx)
            if pos > 0:  # Make sure we're not at the first row
                iti_offsets.append(df_subset.index[pos - 1])
        #Append onset to list of onsets
        iti_offsets_all.extend(iti_offsets)

    # Sort the lists to ensure proper pairing
    iti_onsets_all.sort()
    iti_offsets_all.sort()
    
    # Fix the loop logic
    for onset in iti_onsets_all:
        offset = next((off for off in iti_offsets_all if off > onset), None)
        
        if offset is not None and offset - onset > 20:  # Fix the condition logic
            df_subset.loc[onset:offset, 'ITI'] = 1
        elif offset is None:  # Only fill to end if no offset found
            df_subset.loc[onset:, 'ITI'] = 1
            
    return df_subset

#The following function will import csvs with an optional setting for filtering by a name fragment in the csv
def import_csvs(folder_path, name_filter=None):
    """
    Import CSV files from a folder into a dictionary of DataFrames
    
    Args:
    folder_path : path to folder containing CSV files
    name_filter : optional string to filter files by name (case-insensitive)
                 Only files containing this string will be imported
    
    Returns:
    dictionary of DataFrames, with filename as key and DataFrame as value
    """
    dataframes = {}
    
    # Get all CSV files in the folder
    folder = Path(folder_path)
    csv_files = list(folder.glob("*.csv"))
    
    # Filter files by name if filter is provided
    if name_filter:
        #Choosing only CSV files that contain selected string
        csv_files = [f for f in csv_files if name_filter.lower() in f.name.lower()]
        print(f"Filtering for files containing '{name_filter}'")
    
    if not csv_files:
        #If there are no csv files then this while return a notice and an empty dataframe
        filter_msg = f" containing '{name_filter}'" if name_filter else ""
        print(f"No CSV files{filter_msg} found in {folder_path}")
        return {}
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            dataframes[csv_file.name] = df
            print(f"Loaded: {csv_file.name}")
        except Exception as e:
            print(f"Error loading {csv_file.name}: {e}")
    
    filter_msg = f" (filtered by '{name_filter}')" if name_filter else ""
    print(f"Successfully loaded {len(dataframes)} CSV files{filter_msg}")
    return dataframes

#Function to export csvs to specified folder
def export_csvs(df_dict, filename, export_path, 
                                  column_to_use=None, fill_missing=None):
    """
    Consolidate dataframes and/or series together and export one csv with column titles corresponding to original data
    
    Args:
    df_dict: dictionary of dataframes or series (key will become column name)
    filename: user-defined filename for the output CSV (without extension)
    export_path: path to export the consolidated CSV
    column_to_use: specific column name to extract from each dataframe (ignored for series)
    fill_missing: how to handle missing values ('forward', 'backward', 'zero', None)
    """
    
    #If there are no dataframes/series in dictionary it will tell you
    if not df_dict:
        print("No dataframes or series to consolidate")
        return None
    
    # Create directory if it doesn't exist
    export_dir = Path(export_path)
    export_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all data series
    data_series = {}
    
    #Check to see if dictionaries are empty and handle both DataFrames and Series
    for key, data in df_dict.items():
        # Check if it's a Series
        if isinstance(data, pd.Series):
            if data.empty:
                print(f"Skipping empty series for key: {key}")
                continue
            data_series[key] = data
            
        # Check if it's a DataFrame
        elif isinstance(data, pd.DataFrame):
            if data.empty:
                print(f"Skipping empty dataframe for key: {key}")
                continue
                
            # Handle column selection for DataFrames
            if column_to_use and column_to_use in data.columns:
                # Use specified column
                data_series[key] = data[column_to_use]
            elif len(data.columns) == 1:
                # Single column dataframe
                data_series[key] = data.iloc[:, 0]
            else:
                # Multiple columns - take the first non-time column
                non_time_cols = [col for col in data.columns if 'time' not in col.lower()]
                if non_time_cols:
                    data_series[key] = data[non_time_cols[0]]
                else:
                    data_series[key] = data.iloc[:, 0]
        else:
            print(f"Skipping unsupported data type for key: {key} (type: {type(data)})")
            continue
    
    if not data_series:
        print("No valid data series found")
        return None
    
    # Concatenate all series into one dataframe
    consolidated_df = pd.concat(data_series, axis=1)
    
    # Handle missing values
    #If there is no values and you select forward, it will take the next available value
    if fill_missing == 'forward':
        consolidated_df = consolidated_df.fillna(method='ffill')
    #If there is no values and you select backward, it will take the last available value
    elif fill_missing == 'backward':
        consolidated_df = consolidated_df.fillna(method='bfill')
    #If there is no values and you select zero, it will fill missing values with 0
    elif fill_missing == 'zero':
        consolidated_df = consolidated_df.fillna(0)
    # If None, leave NaN values as is
    
    # Export the consolidated dataframe
    file_path = export_dir / f"{filename}.csv"
    consolidated_df.to_csv(file_path, index=True)
    
    print(f"Consolidated dataframe exported to: {file_path}")
    print(f"Shape: {consolidated_df.shape}")
    print(f"Columns: {list(consolidated_df.columns)}")
    print(f"Index range: {consolidated_df.index.min()} to {consolidated_df.index.max()}")
    
    return consolidated_df

#Function to average specified data around specified events, creating a timeseries
def average_around_timestamp(df_subset,value_column, event_column, time_before=15, time_after=45):
    """
    Args:
    df_subset : subsetted behavior data
    event_column : column name to detect events (0->1 transitions)
    value_column : column of data to quantify
    time_before : time before onset to include in analysis (seconds)
    time_after : time after onset to include in analysis (seconds)
    """
    
    # Get onset timestamps (0->1 transitions)
    onset_mask = (df_subset[event_column] > 0) & (df_subset[event_column].diff() > 0)
    onset_timestamps = df_subset[onset_mask].index
    
    # Check that there are timestamps for this column
    if len(onset_timestamps) == 0:
        print(f"No onsets found for {event_column}")
        return pd.DataFrame()
    
    # Store all event-aligned data
    aligned_data = []
    
    # Loop through each onset timestamp
    for timestamp in onset_timestamps:
        # Define time window around the event
        start_time = timestamp - time_before
        end_time = timestamp + time_after
        
        # Select data within the time window
        mask = (df_subset.index >= start_time) & (df_subset.index <= end_time)

        window_data = df_subset.loc[mask, value_column].copy()
        
        if len(window_data) == 0:
            continue
            
        # Create relative time index (seconds from onset)
        relative_times = df_subset.loc[mask].index - timestamp
        
        # Create a series with relative time as index
        event_series = pd.Series(window_data.values, index=relative_times)
        aligned_data.append(event_series)
    
    if not aligned_data:
        print("No valid data windows found")
        return pd.DataFrame()
    
    # Combine all events into a DataFrame
    result_df = pd.DataFrame(aligned_data).T
    
    # Calculate mean across all events
    mean_timeseries = result_df.mean(axis=1)
    
    return mean_timeseries

#Function to create a histogram of nosepoking activity over the course of the task into time bins
def behavior_binning(df, value_column, event_column=None, bin_size=30, beh_freq = 2):
    """    
    Args:
    df : input downsampled dataframe to analyze
    value_column : behavior to quantify in the histogram
    event_column : column to extract specific timepoints when the variable is active (column value is 1). 
                   Requires at least 2 events per bin. Set to None by default
    bin_size : size of time bins in seconds to create histogram, automatically set to 30 second bins
    beh_freq : frequency in Hz of downsampled behavior df. Default set to 2 Hz
    
    Returns:
    pandas.Series: Index is time axis (bin start times), values are the binned behavioral counts
    """
    
    # Find the length of the input dataframe
    total_time = df.index[-1]
    
    # Calculate the total number of bins to be created
    num_bins = int(total_time // bin_size)  # Fixed: convert to int and use floor division
    
    # Initiate lists to track the number of nosepokes as well as the start time for the bin
    sum_nosepoke = []
    time_axis = []
    
    for i in range(num_bins):
        # Designate the start of the bin
        start = i * bin_size
        # Designate the end of the bin
        end = start + bin_size
        
        # Bin the data and select the column of interest
        bin_data = df[(df.index >= start) & (df.index < end)][str(value_column)]
        
        # Append the data to the growing list
        sum_nosepoke.append((bin_data.sum()/(bin_size*beh_freq)*100))
        time_axis.append(start)
    
    # Cue aligned binning
    if event_column is not None:
        # Create filtered lists for cue-aligned data
        cue_aligned_counts = []
        cue_aligned_times = []
        
        # Loop through each bin and check if there's an event during that time window
        for i, start_time in enumerate(time_axis):
            end_time = start_time + bin_size
            
            # Check if there are events (value of 1) in the event_column during this bin
            bin_events = df[(df.index >= start_time) & (df.index < end_time)][event_column]
            
            # If there are at least two events (value of 1) in this bin, include it
            if (bin_events == 1).sum() >= 2:
                cue_aligned_counts.append(sum_nosepoke[i])
                cue_aligned_times.append(start_time)
        
        # Return cue-aligned data as pandas Series
        import pandas as pd
        return pd.Series(data=cue_aligned_counts, index=cue_aligned_times)
    
    else:
        # Return all data as pandas Series
        import pandas as pd
        return pd.Series(data=sum_nosepoke, index=time_axis)
    
#Function to calculate the auc from input csvs that have are outputs from above average around timestamps function
def calculate_auc(df, start=0, end=30):
    """
    Function to calculate the AUC over a designated timeframe from an already processed dataset

    Args:
    df : timeseries data csv where the index is time aligned to cue onset
    start : index to start the AUC calculation. Automatically set to 0, or when the cue starts
    end : index to for when to end the AUC calculation, typically when the cue turns off. Automatically set to 30, or 30 seconds after cue onset
    
    returns a pandas series where the index is the column name for the auc calculation
    """

    #Set the time column as your index
    df_set = df.set_index('TIME (S)').copy()

    #Select only the data between start and end timepoints using .loc, which uses index names
    data_snip = df_set.loc[start:end]

    #Initialize dictionary to store data
    auc_data={}

    #Use a for loop to calculate the AUC for each column and store data in a dictionary
    for mouse, data in data_snip.items():
        #Take the length of the index and arrange them in order from 1-end value
        x=np.arange(len(data)) 
        #Define your y values as the value associated with each index value in order
        y=data.values
        #Use the trapezoidal rule to calculate AUC
        auc=trapezoid(y,x)

        auc_data[mouse]=float(auc)
    
    return pd.Series(auc_data)

#Function to calculate average mounting speed before mounting the platform
def mount_speed(df, event_column, start_time=0, end_time=None):
    """
    Function to calculate the average speed of platform mounting transitions that occur during an event,
    within a specific time window after event onset
    
    Args:
    df : dataframe containing processed and downsampled behavior data
    event_column : column name indicating when the event of interest is active (1) or inactive (0)
    start_time : float, time in seconds after event onset to start analysis (default: 0)
    end_time : optional float, time in seconds after event onset to end analysis.
               If None, analyzes until the event ends
    
    Returns: 
    float - average speed of all mounting transitions that occur during the specified time period
    """
    
    # Find all platform mounting transitions (0 -> non-zero)
    platform_values = df['IN PLATFORM']
    mount_mask = (platform_values == 0) & (platform_values.shift(-1) > 0)
    
    if start_time == 0 and end_time is None:
        # Use entire event duration
        event_active_mask = df[event_column] == 1
        time_description = "entire event duration"
    else:
        # Find event onset points (0 -> 1 transitions)
        event_onset_mask = (df[event_column] == 1) & (df[event_column].diff() == 1)
        event_onset_times = df[event_onset_mask].index
        
        if len(event_onset_times) == 0:
            print(f"No event onsets found for {event_column}")
            return np.nan
        
        # Create mask for time windows after each onset
        event_active_mask = pd.Series(False, index=df.index)
        
        #Iterate through each onset time and subset the tone period
        for onset_time in event_onset_times:
            window_start = onset_time + start_time
            
            if end_time is None:
                # Find when this specific event ends
                event_end_mask = (df[event_column] == 0) & (df[event_column].shift(1) == 1)
                subsequent_ends = df[event_end_mask].index[df[event_end_mask].index > onset_time]
                
                if len(subsequent_ends) > 0:
                    window_end = subsequent_ends[0]
                else:
                    window_end = df.index[-1]  # Use end of dataframe if event doesn't end
            else:
                window_end = onset_time + end_time
            
            window_mask = (df.index >= window_start) & (df.index <= window_end)
            event_active_mask = event_active_mask | window_mask
        
        # Create time description
        if end_time is None:
            time_description = f"from {start_time}s after onset until event end"
        else:
            time_description = f"from {start_time}s to {end_time}s after event onset"
    
    # Find mounting transitions that occur during the specified time period
    mounts_during_event = mount_mask & event_active_mask
    
    if not mounts_during_event.any():
        print(f"No platform mounting transitions found during {time_description} of {event_column}")
        return 0,0
    
    # Get the speed values at these mounting transitions
    mount_speeds = df.loc[mounts_during_event, 'SPEED (M/S)']
    
    # Calculate and return the average speed
    average_speed = mount_speeds.mean()
    
    return len(mount_speeds),average_speed

#Function to split up dataframe for more fine-tuned analysis
def split_dfs(df, event_column, subset_start, subset_end, baseline=300):
    """
    Function to split dataframes into smaller sections to analyze specific parts of the data (early, late, etc.)
    
    Args:
    df : Input downsampled and processed dataframe
    event_column : column to use to subset data
    subset_start : what instance of event_column to start the slice. 0 would be the first instance, 1 second, etc.
    subset_end : what instance of event_column to end the slice. -1 would be the last, -2 second to last, etc.
        If using positive numbers, remember that 5 would be the 6th occurence, 7 would be the 7th, etc.
    baseline : seconds before onset to include as a baseline period. Default is 300 seconds
    
    Returns:
    df_slice : smaller dataframe with specific timeframe
    """
    
    # Find event onset points (0 -> 1 transitions)
    event_onset_mask = (df[event_column] == 1) & (df[event_column].diff() == 1)
    true_indices = event_onset_mask[event_onset_mask].index
    onsets = true_indices.tolist()
    
    # Check if we have enough onsets
    if len(onsets) == 0:
        print(f"No event onsets found for {event_column}")
        return df.iloc[0:0].copy()  # Return empty dataframe with same structure
    
    # Handle negative indices for subset_end
    if subset_end < 0:
        actual_subset_end = len(onsets) + subset_end
    else:
        actual_subset_end = subset_end
    
    # Validate indices and let the user know there is an error if invalid
    if subset_start >= len(onsets) or actual_subset_end >= len(onsets) or subset_start > actual_subset_end:
        print(f"Invalid subset indices. Available onsets: {len(onsets)}, requested: {subset_start} to {subset_end}")
        return df.iloc[0:0].copy()  # Return empty dataframe
    
    # Determine start and end times for slicing
    start_time = onsets[subset_start] - baseline
    
    # For end time, we need to either:
    # 1. Go to the next onset after subset_end (if it exists)
    # 2. Or find when the event at subset_end actually ends
    # 3. Or use the end of the dataframe
    
    if actual_subset_end + 1 < len(onsets):
        # Use the next onset as the end point
        end_time = onsets[actual_subset_end + 1] - 1
    else:
        # Use the end of the dataframe
        end_time = df.index[-1]  # Use end of dataframe
    
    # Ensure start_time and end_time are within dataframe bounds
    start_time = max(start_time, df.index[0])
    end_time = min(end_time, df.index[-1])
    
    # Slice the dataframe using .loc for label-based indexing
    df_slice = df.loc[start_time:end_time].copy()
    
    print(f"Sliced dataframe from {event_column} onset {subset_start} to period following {event_column} {(subset_end+1)}")
    print(f"Time range: {start_time} to {end_time}")
    print(f"Resulting dataframe shape: {df_slice.shape}")
    
    return df_slice

#Function to assign some sort of behavioral task strategy value
def task_strat(df, event_column=None, beh_freq=2):
    """
    Args:
    df: downsampled and processed behavior dataframe
    event_column: optional argument to evaluate task strategy during certain task phases, such as CS+ or CS-.
    beh_freq : frequency in Hz of downsampled behavior df. Default set to 2 Hz
    
    Returns:
    task_score: a value from -1 to 1 indicating the task strategy.
        A value of 1 indicates a compulsive strategy, the mouse is constantly nosepoking for reward and not on platform
        A value of 0 indicates a balanced strategy where the mouse is spending equal time nosepoking and on platform
        A value of -1 indicates an avoidant strategy where the mouse stays on the platform consistently
    """

    #First, create a mask to only select indices for when the house light or speaker is on
    if event_column is None:
        activity_mask= (df['CUE LIGHT ACTIVE'] > 0) | (df['NEW SPEAKER ACTIVE'] > 0)
        activity_df = df[activity_mask].copy()
    else:
        activity_mask= ((df['CUE LIGHT ACTIVE'] > 0) | (df['NEW SPEAKER ACTIVE'] > 0)) & (df[event_column] > 0)
        activity_df = df[activity_mask].copy()
        
    #Second, use this mask to sum nosepoke and time on platform values
    plat_time = activity_df['IN PLATFORM'].sum()
    np_time = activity_df['NOSE POKE ACTIVE'].sum()

    #Third, use these values to calculate score. Divide both by greater value, if Plat is greater take negative dividend
    #of np, if np is greater take positive divident of plat, and if plat is 0 make value 1 and if np is 0 make value -1.
    if plat_time>np_time:
        task_score = (1-(np_time/plat_time))*-1
    elif np_time>plat_time:
        task_score = (1-(plat_time/np_time))
    elif np_time == plat_time:
        if plat_time == 0 & np_time == 0:
            print('No values in platform or nosepoke column')
            return None
        else:
            task_score = 0
    elif np_time == 0:
        task_score = -1
    elif plat_time == 0:
        task_score = 1

    #Finally, return this value in a list along with total TOP and NP
    return [task_score, (plat_time/beh_freq), (np_time/beh_freq)]

#Function to further process variable PMA by creating Light Only, Tone Only, Copresentation, Tone then Light, and Light then Tone binary columns
def overlap_beh_processing(df):
    """ 
    Args:
    df: processed dataframe
    
    Returns:
    df_proc: further processed dataframe to include additional binary columns
    """

    df_proc = df.copy()

    #Utilize NEW SPEAKER ACTIVE AND CUE LIGHT ON columns and the overlap of the columns to create new columns
    #Get onset timestamps for both event columns
    light_mask = (df_proc['CUE LIGHT ACTIVE'] > 0) & (df_proc['CUE LIGHT ACTIVE'].diff() > 0)
    light_timestamps= df_proc[light_mask].index

    # Check that there are timestamps for this column
    if len(light_timestamps) == 0:
        print(f"No onsets found for 'CUE LIGHT ACTIVE'")
        return pd.DataFrame()

    tone_mask= (df_proc['NEW SPEAKER ACTIVE']>0) & (df_proc['NEW SPEAKER ACTIVE'].diff() > 0)
    tone_timestamps = df_proc[tone_mask].index

    # Check that there are timestamps for this column
    if len(tone_timestamps) == 0:
        print(f"No onsets found for {'NEW SPEAKER ACTIVE'}")
        return pd.DataFrame()
        
    #initiate lists for iteration of timestamps
    ltt_timestamps=[]
    ttl_timestamps=[]
    light_only_timestamps=[]
    tone_only_timestamps=[]
    cop_timestamps=[]
    used_light = set()
    used_tone = set()

    #Look through timestamps and set light then tone onsets
    for i, light in enumerate (light_timestamps):
        for j, tone in enumerate (tone_timestamps):
            #Create copresentation timestamps
            if abs(light-tone) <=1 :
                #Add timestamps from light column to copresentation timestamp list
                cop_timestamps.append(light)
                #Mark index for light as used so that it is not included again
                used_light.add(i)
                used_tone.add(j)
                break #move to next number in onset_timestamps_1

            #Create light then tone timestamps
            elif -20 < light-tone < -5: #If the light presentation comes first
                #Add timestamp from light column to ltt column
                ltt_timestamps.append(light)
                #Mark index for both indices as used
                used_light.add(i)
                used_tone.add(j)
                break #move to next number in onset_timestamps_1
            
            #Create tone then light timestamps
            elif 5 < light-tone < 20: #If the tone presentation comes first
                #Add timestamp from light column to ltt column
                ttl_timestamps.append(tone)
                #Mark index for light as used so that it is not included again
                used_light.add(i)
                used_tone.add(j)
                break #move to next number in onset_timestamps_1

            #Create light only timestamps
            elif j == (len(tone_timestamps)-1): #If values don't overlap add to light only list on last iteration
                #add lower number to list
                light_only_timestamps.append(light)
                #Mark index for light as used so that it is not included again
                used_light.add(i)
                break #move to next number in onset_timestamps_1

            else:
                print(f'None type for light onset {i}, {light}')
    
    #Create tone only timestamps
    for i, tone in enumerate (tone_timestamps):
        if i in used_tone:
            continue
        else:
            tone_only_timestamps.append(tone)

    #Create columns for each presentation type
    df_proc['LIGHT ONLY'] = 0
    df_proc['TONE ONLY'] = 0
    df_proc['CO-PRESENTATION'] = 0
    df_proc['TONE THEN LIGHT'] = 0
    df_proc['LIGHT THEN TONE'] = 0

    #Use onset timestamps to fill dataframe
    for onset in light_only_timestamps:
        df_proc.loc[onset:onset+30, 'LIGHT ONLY'] = 1
    
    for onset in tone_only_timestamps:
        df_proc.loc[onset:onset+30, 'TONE ONLY'] = 1

    for onset in cop_timestamps:
        df_proc.loc[onset:onset+30, 'CO-PRESENTATION'] = 1

    for onset in ttl_timestamps:
        df_proc.loc[onset:onset+45, 'TONE THEN LIGHT'] = 1

    for onset in ltt_timestamps:
        df_proc.loc[onset:onset+45, 'LIGHT THEN TONE'] = 1

    return df_proc

#Function to count number of avoided shocks
def avoid_shock(df, shock_length=2.5):
    """
    Args:
    df: downsampled and processed dataframe
    shock_length: length of administered shock (in seconds)
    
    Returns:
    shock_list: list of cumulative avoided shock counts
    """
    # Create mask for shock onsets
    shock_mask = (df['NEW SHOCKER ACTIVE'] > 0) & (df['NEW SHOCKER ACTIVE'].diff() > 0)
    shock_timestamps = df[shock_mask].index

    # Check that there are onsets
    if len(shock_timestamps) == 0:
        print("No shock onsets found")
        return []
    
    # Store shock outcomes
    shock_count = 0
    shock_list = []

    # Loop through timestamps and determine if shock was avoided
    for timestamp in shock_timestamps:
        # Get the time window for this shock
        end_time = timestamp + shock_length
        shock_window = df.loc[timestamp:end_time, 'IN PLATFORM']
        
        # Calculate actual time duration and occupancy
        shock_duration = len(shock_window)
        time_on_plat = shock_window.sum()
        
        # Check if shock was avoided (with tolerance for minor gaps)
        if time_on_plat == shock_duration:
            shock_count += 1
            
        shock_list.append(shock_count)

    return shock_list
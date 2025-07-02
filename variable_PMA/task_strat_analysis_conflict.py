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
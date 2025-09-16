if input('Combine CS+ and CS- histograms into protocol order? Y/N: ') in ('Y', 'y'):
    # Ask user for file paths instead of relying on hardcoded names
    cs_plus_path = input("Please enter FULL path to CS+ histogram CSV: ").strip()
    cs_minus_path = input("Please enter FULL path to CS- histogram CSV: ").strip()
    protocol_path = input("Please enter FULL path to protocol CSV: ").strip()
# Check that all files exist
for f in [cs_plus_path, cs_minus_path, protocol_path]:
    if not os.path.exists(f):
        raise FileNotFoundError(f"\n:x: Could not find required file:\n{f}\n")

# Load histograms
cs_plus_df = pd.read_csv(cs_plus_path)
cs_minus_df = pd.read_csv(cs_minus_path)

# Load protocol and clean column names
protocol_df = pd.read_csv(protocol_path)
protocol_df.columns = protocol_df.columns.str.strip()

# Extract trial order info
trial_order = protocol_df[['Trial Number', 'Tone start', 'CS+(1) CS-(2)']].copy()
trial_order.rename(columns={'Tone start': 'Time (s)', 'CS+(1) CS-(2)': 'CS Type'}, inplace=True)
trial_order['CS Type'] = trial_order['CS Type'].map({1: 'CS+', 2: 'CS-'})

# Function to melt histogram into long format
def melt_hist(df, cs_type):
    """Reshape histogram from wide (animals as columns) to long format."""
    df_long = df.melt(id_vars=df.columns[0], var_name='Animal', value_name='Value')
    df_long.rename(columns={df.columns[0]: 'Time (s)'}, inplace=True)
    df_long['CS Type'] = cs_type
    return df_long

# Melt and combine CS+ and CS- histograms
cs_plus_long = melt_hist(cs_plus_df, 'CS+')
cs_minus_long = melt_hist(cs_minus_df, 'CS-')
combined_long = pd.concat([cs_plus_long, cs_minus_long], ignore_index=True)

# Merge with trial order to ensure protocol sorting
merged = trial_order.merge(combined_long, on=['Time (s)', 'CS Type'], how='left')
merged.sort_values(['Trial Number', 'Animal'], inplace=True)

# Pivot so each trial is one row with all animals as columns
pivot_df = merged.pivot_table(index=['Trial Number', 'Time (s)', 'CS Type'],
columns='Animal',
values='Value').reset_index()
pivot_df.columns.name = None # remove pivot index name

# Add previous trial type and sequence info
merged['Prev CS Type'] = merged.groupby('Animal')['CS Type'].shift(1)
merged['Sequence'] = merged['Prev CS Type'] + " → " + merged['CS Type']

# === BIN-LEVEL SEQUENCE SUMMARY ===
# Average across ALL time bins for each Animal × Sequence
summary_df = merged.groupby(['Animal', 'Sequence'])['Value'].mean().reset_index()

# === TRIAL-LEVEL SEQUENCE SUMMARY ===
# Step 1: sum within each trial (total response over the whole trial window)
trial_sums = merged.groupby(['Animal', 'Sequence', 'Trial Number'])['Value'].sum().reset_index()

# Step 2: average these trial totals for each Animal × Sequence
trial_level_summary_df = trial_sums.groupby(['Animal', 'Sequence'])['Value'].mean().reset_index()

# Save all outputs
export_folder = input("Please enter FOLDER path to save outputs: ").strip()
os.makedirs(export_folder, exist_ok=True)
pivot_path = os.path.join(export_folder, "combined_histograms_pivoted.csv")
annotated_path = os.path.join(export_folder, "combined_histograms_with_sequence.csv")
summary_path = os.path.join(export_folder, "sequence_effect_summary_bin_level.csv")
trial_level_summary_path = os.path.join(export_folder, "sequence_effect_summary_trial_level.csv")
pivot_df.to_csv(pivot_path, index=False)
merged.to_csv(annotated_path, index=False)
summary_df.to_csv(summary_path, index=False)
trial_level_summary_df.to_csv(trial_level_summary_path, index=False)

# Status messages
print(f"\n:white_check_mark: Combined pivoted histogram saved to: {pivot_path}")
print(f":white_check_mark: Annotated trial data saved to: {annotated_path}")
print(f":white_check_mark: Bin-level mean summary saved to: {summary_path}")
print(f":white_check_mark: Trial-level summed→average summary saved to: {trial_level_summary_path}")
ran_analysis.append('Combined Histograms & Sequence Analysis')
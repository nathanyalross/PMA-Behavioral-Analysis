# PMA-Behavioral-Analysis
A python based behavioral analysis pipeline designed to analyze mouse behavior in the platform mediated avoidance task with functions that are flexible for different versions of the task.

## Code Installation 
To best utilize and customize this pipeline I recommend downloading and using Visual Studio Code at https://code.visualstudio.com/download.

Once Visual Studio code is installed you can clone the git repo using web URL or download a zip file containing all of the code under the 'Code' tab above.

## UV
Once the pipeline is installed on your computer you will need to download UV to ensure you have everything you need for the code to run properly.

### Installing UV
Install UV through the powershell using installation instructions outlined here: https://docs.astral.sh/uv/getting-started/installation/.

Check that UV is installed by checking the version:
`uv --version`

### Installing dependencies through UV
Once UV is installed to your computer, you can install all needed dependencies with `uv sync`

After downloading the dependencies initiate a local virtual environment with `uv venv`

To check that you have all necessary dependencies run `uv pip list` and make sure you have everything specified in the 'pyproject.toml' file

## Pipeline Inputs 
The input to this pipeline is behavior timeseries CSVs, this was initially designed for AnyMaze outputs. Include all outputs that contain behavioral information and cue information.

## Outputs
This pipeline will have default outputs that are easily customizable. These include:

1) Timeseries data that is averaged across a session around a repeated event, such as a cue.
2) Histograms generated across specified cues or across an entire session.
3) Calculations of the AUC of timeseries data.
4) Task strategy score calculations to show how mice are behaving in different phases of the task - are they 'compulsive' or 'aversive'?
5) Platform mount transition analysis to see how mice are approaching the platform during different phases of the task.

The functions this pipeline uses is designed to be easily adjusted for case-by-case use.

## Designed use and adaptability
The default scripts are designed to be used in a two-tone discrimation PMA task, where there are two stages: the reward learning stage where mice learn to nosepoke during cue light presentation for reward, and a discrimination stage where mice are presented tones and cue-lights together with two different frequency tones predicting a shock or no shock.

All functions are extensively documented to outline how to adapt parameters to your use. Make sure to read through all scripts and adjust as needed. Beginner-level python experience is helpful to adjust parameters.

## The basics - using a pre-made pipeline in VS Code
Navigate to File->Open Folder

Open Project Folder

Open powershell with ctr+`; type cd\folder_for_PMA_variation

In powershell enter `py process_rew_data.py`, this will run the script to process timeseries data for reward phase.

If processing discrimination phase data, enter `py process_disc_data.py`

Use same `py scripy.py` logic to run any other script!
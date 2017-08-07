# FolderCleaner
The general idea for the script is pretty straight forward, delete files older than a specified number days. The script is a fully capable command line tool. The UI is a very basic cross platform UI to engage the script without any terminal knowledge/experience.

The command line script is capable of handling as many paths as are passed in, but all paths will be processed using the same parameters. 

### Script Options 
- Flags
    - -p --path       (Path to parse (required))
    - -d --days       (Overwrite the default age parameter (default: 7))
    - -f --files      (Delete files only. Skip empty direcories)
    - -v --verbose    (Verbose Output)
    - -s --silent     (Silence all output)
    - -t --testonly   (Run script with semi-verbosity and no deletes)

### UI Specific Options
- The UI only supports up to five folders in a batch.
- VERBOSE will output all actions the script completes to the output window
- SILENT will prevent any output from occuring
- FILES ONLY will only process files, and will not delete any empty folders found
- TEST ONLY will show all actions that will occur, but will not delete any files/folders. In the UI this is on by default to prevent any accidental deletion.
- The number of days is set to determine the minimum time since the last modified date to qualify for deletion. If last modified date is older than set watermark it is set for deletion.
- PROCESS will process the job according to settings"

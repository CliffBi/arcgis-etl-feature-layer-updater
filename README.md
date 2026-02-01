# ArcGis ETL Feature layer updater (Test Project)
Test project designed to fetch data from Google Spreadsheets, process it, and upload it to an ArcGIS FeatureLayer.
This project implements two ways of interacting with sheets: by name and by GID.

## Description
The project provides two ways to interact with a sheet in a spreadsheet. The first method is via Sheet Name 
(`run_upload_data`), and the second is via Sheet GID (`run_upload_data_by_gid`). 
This approach was chosen to demonstrate the possible interaction methods. Additionally, interaction via Sheet Name is 
flexible, while interaction via GID is strict. 
This behavior is also documented in the `SpreadSheetProvider` and `GidSpreadSheetProvider` classes.

## Requirements
### Python
#### Version: 3.11

## Beginning of work
#### [Ubuntu] To run the project, you need to:
1. Rename the file example.env to .env and configure it for use.
2. execute command in bash `pip install -r requirements.txt` for install libs or `pip install -r requirements-dev.txt` 
if you want to use dotenv lib. 
3. execute command in bash `python run.py` to run the program or `python run_using_gid.py` to run program using `GidSpreadSheetProvider`.

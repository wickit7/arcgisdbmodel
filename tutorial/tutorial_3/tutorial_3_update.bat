@echo off
chcp 65001

rem create datamodel with JSON
"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "..\..\create_db_model.py" "tutorial_3_update.json"

pause



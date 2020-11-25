@echo off
set "script_path=%~dp0"
set "script_path=%script_path%pypassmanager.py"
python %script_path% %*
@echo off
copy /y UiScriptLibCythonizer.bat UiScriptLib\
copy /y UiScriptLibCythonizer.py UiScriptLib\
cd UiScriptLib\
call UiScriptLibCythonizer.bat
REM pause

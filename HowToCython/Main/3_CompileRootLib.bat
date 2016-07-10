@echo off
copy /y RootLibCythonizer.bat RootLib\
copy /y RootLibCythonizer.py RootLib\
cd RootLib\
call RootLibCythonizer.bat
REM pause

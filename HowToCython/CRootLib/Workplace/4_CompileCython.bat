@echo off
copy /y MakeFile_VC_Release.bat RootLib\cyTemp\
cd RootLib\cyTemp\
call MakeFile_VC_Release.bat
pause

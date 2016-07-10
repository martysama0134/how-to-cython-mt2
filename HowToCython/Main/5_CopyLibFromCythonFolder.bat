@echo off
mkdir out
copy /y RootLib\PythonrootlibManager.cpp out\
copy /y RootLib\PythonrootlibManager.h out\
copy /y RootLib\cyTemp\rootlib.lib out\
echo copy completed
pause

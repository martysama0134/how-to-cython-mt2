@REM ### Compiler Folder
@REM ## vs2008 9.0
@REM @SET VSINSTALLDIR=C:\Program Files (x86)\Microsoft Visual Studio 9.0
@REM @SET VCINSTALLDIR=C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC
@REM ## vs2010 10.0
@REM @CALL "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat"
@SET VSINSTALLDIR=C:\Program Files (x86)\Microsoft Visual Studio 10.0
@SET VCINSTALLDIR=C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC
@REM ## vs2012 11.0
@REM @CALL "C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\vcvarsall.bat"
@REM @SET VSINSTALLDIR=C:\Program Files (x86)\Microsoft Visual Studio 11.0
@REM @SET VCINSTALLDIR=C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC
@REM ## vs2013 12.0
@REM @CALL "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat"
@REM @SET VSINSTALLDIR=C:\Program Files (x86)\Microsoft Visual Studio 12.0
@REM @SET VCINSTALLDIR=C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC

@REM ### Python Folder
@SET PYTHONLIBSPATH=C:\Python27\libs
@SET PYTHONINCLUDEPATH=C:\Python27\include

@SET FrameworkDir=Framework32
@SET FrameworkVersion=v2.0.50727
@if "%VSINSTALLDIR%"=="" goto error_no_VSINSTALLDIR
@if "%VCINSTALLDIR%"=="" goto error_no_VCINSTALLDIR

@echo Setting environment for using Microsoft Visual Studio 2008 x86 tools.

@call :GetWindowsSdkDir

@if not "%WindowsSdkDir%" == "" (
	set "PATH=%WindowsSdkDir%bin;%PATH%"
	set "INCLUDE=%WindowsSdkDir%include;%INCLUDE%"
	set "LIB=%WindowsSdkDir%lib;%LIB%"
)


@rem
@rem Root of Visual Studio IDE installed files.
@rem
@set DevEnvDir=%VSINSTALLDIR%\Common7\IDE

@set PATH=%DevEnvDir%;%VCINSTALLDIR%\BIN;%VSINSTALLDIR%\Common7\Tools;%VSINSTALLDIR%\Common7\Tools\bin;%FrameworkDir%\%Framework35Version%;%FrameworkDir%\%Framework35Version%\Microsoft .NET Framework 3.5 (Pre-Release Version);%FrameworkDir%\%FrameworkVersion%;%VCINSTALLDIR%\VCPackages;%PATH%
@set INCLUDE=%VCINSTALLDIR%\ATLMFC\INCLUDE;%VCINSTALLDIR%\INCLUDE;%INCLUDE%
@set LIB=%VCINSTALLDIR%\ATLMFC\LIB;%VCINSTALLDIR%\LIB;%LIB%
@set LIBPATH=%FrameworkDir%\%Framework35Version%;%FrameworkDir%\%FrameworkVersion%;%VCINSTALLDIR%\ATLMFC\LIB;%VCINSTALLDIR%\LIB;%LIBPATH%

@goto end

:GetWindowsSdkDir
@call :GetWindowsSdkDirHelper HKLM > nul 2>&1
@if errorlevel 1 call :GetWindowsSdkDirHelper HKCU > nul 2>&1
@if errorlevel 1 set WindowsSdkDir=%VCINSTALLDIR%\PlatformSDK\
@exit /B 0

:GetWindowsSdkDirHelper
@SET WindowsSdkDir=
@for /F "tokens=1,2*" %%i in ('reg query "%1\SOFTWARE\Microsoft\Microsoft SDKs\Windows" /v "CurrentInstallFolder"') DO (
	if "%%i"=="CurrentInstallFolder" (
		SET "WindowsSdkDir=%%k"
	)
)
@if "%WindowsSdkDir%"=="" exit /B 1
@exit /B 0

:error_no_VSINSTALLDIR
@echo ERROR: VSINSTALLDIR variable is not set.
@goto end

:error_no_VCINSTALLDIR
@echo ERROR: VCINSTALLDIR variable is not set.
@goto end

:end

set lib=%lib%;%PYTHONLIBSPATH%;
set include=%include%;%PYTHONINCLUDEPATH%;
cl /Od /D "WIN32" /D "_DEBUG" /D "_WINDOWS" /D "USE_LOD" /D "_VC80_UPGRADE=0x0710" /D "_MBCS" /FD /EHsc /RTC1 /MTd /W3 /nologo /c /Zi /MP8 *.c
lib /out:.\rootlib_d.lib *.obj
pause

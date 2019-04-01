1. Download the latest python2.7 version (2.7.16 right now) from here:

	https://www.python.org/downloads/

	https://www.python.org/ftp/python/2.7.16/python-2.7.16.msi

	Check the correct one you need.

2. Install it specifying the "Add python.exe to PATH" like [this](https://i.imgur.com/o4IxRhr.png)

3. Download VS2017 (or vs2019) Community from here:

	https://visualstudio.microsoft.com/it/downloads/

4. From Visual Studio Installer, specify just the "desktop c++" environment like [this](https://i.imgur.com/tCOX2ui.png) (mfc/atl/cmake not needed) and install it

5. In `C:\Python27\Lib\distutils\msvc9compiler.py` replace the whole `find_vcvarsall` function with this:

	```python
	def find_vcvarsall(version):
	    return r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars32.bat" #or vcvarsall.bat
	```
	_Note: use 4 spaces instead of 1 tab for indentation._

6. Open cmd, and write:
	```batch
	C:\Python27
	cd scripts
	python -m pip install --upgrade pip
	pip install cython
	```


------------------------------------------
# Table of Contents

* [Intro](#intro)
* [Is Cython really worth it?](#is-cython-really-worth-it)
* [Download](#download)
* [VideoTutorial](#videotutorial)
* [FAQs](#faqs)

------------------------------------------
## Intro
This repository will explain how to "convert" your root .py files to .c ones.

Actually, Cython only converts those files to pure CPython code.


------------------------------------------
## Is Cython really worth it?

* Pros
    * All the modules are compiled, and they can't be "extracted as .py" anymore.

      We can always disassemble the launcher with IDA, but the result will be pseudo-c code after waiting 6-8h of analyzing.

    * Since we're not using **.pyx** files but directly **.py** ones, there's no "so much optimization".

      At least, 10% of performance increasing is guaranteed.

* Cons

    * For testing purposes, it's heavy to maintain. Everytime you try to re-compile your root files, you should wait 5-10 minutes.

      You can always use the uncythonized root (.py files) when you perform tests, and compile cython whenever you will make an update in your live server.

    * The launcher's size will increase ~10mb. You can actually pack it to save space.

      If you directly use a .pyd (still 10mb), the launcher's size won't increase.

------------------------------------------
## Download

[HowToCython.zip](https://github.com/martysama0134/how-to-cython-mt2/archive/master.zip)

Such archive contains the following things:

* Main\ -> It contains all the required files to build the rootlib.lib file
    * HOW-TO-CYTHON.txt -> A complete tutorial of everything you need to do for rootlib (and list of issues)

* UiMain\ -> It contains all the required files to build the uiscriptlib.lib file
    * HOW-TO-EXTRA-CYTHON.txt -> A complete tutorial of everything you need to do for uiscriptlib

* Extra\
    * root\
        * system.py -> From the official cn's root dated 2014/01/01 with the cython implementation inside (for rootlib)
        * ui.py -> From the official cn's root dated 2014/01/01 with the "extra" cython implementation inside (for uiscriptlib)
    * rootlibpyd\ -> A sample project to build your own rootlib.pyd
    * uiscriptlibpyd\ -> A sample project to build your own uiscriptlib.pyd

------------------------------------------
## VideoTutorial

> [How-To] Metin2 & Cython - Part 1 - Build rootlib

[![Video Label](http://img.youtube.com/vi/wQ5GfUopy58/0.jpg)](http://www.youtube.com/watch?v=wQ5GfUopy58)

> [How-To] Metin2 & Cython - Part 2 A - Build metin2client with rootlib linked inside

[![Video Label](http://img.youtube.com/vi/qHB4EGed6Ts/0.jpg)](http://www.youtube.com/watch?v=qHB4EGed6Ts)

> [How-To] Metin2 & Cython - Part 2 B - Build a PYD from rootlib

[![Video Label](http://img.youtube.com/vi/iMt0SiO3sQI/0.jpg)](http://www.youtube.com/watch?v=iMt0SiO3sQI)

> [How-To] Metin2 & Cython - Part 3 - Build uiscriptlib and use it as PYD

[![Video Label](http://img.youtube.com/vi/gdoD7YdCVQ0/0.jpg)](http://www.youtube.com/watch?v=gdoD7YdCVQ0)

------------------------------------------
## FAQs

### Q1
> I think you should make a guide of how to repair the errors given by the **.py** files when you are cythonicing, since a lot of people don't know what to do in these cases.

### A1
The only two errors you could get when you compile your root are:

* "Decoding error, missing or incorrect coding"

  Since all the .py files are processed as korean strings, all the ones written with a different charset (arabic) will trigger this issue.

  It's explained in the .txt file, and you can simply bypass this just writing the text in the locale_game.txt file.

  You can also specify the charset to use just adding something like this at the beginning of the .py file:

  ```python
  # -*- coding: cp1252 -*-
  ```

  Note:
  
    * cp1252 = latin1 charset! _(save the document as ansi)_

    * cp1256 = arabic charset! _(save the document as ansi)_

    * utf-8 = unicode charset! _(save the document as unicode w/o BOM)_

* "Expected an increase in indentation level" or similar

  This happens when the .py file has a bad tabulation, so bad written:

  It's clear that you won't be able to compile unworkable/unrunnable/broken .py files.

------------------------------------------
### Q2
> Can you cythonize all the python files of the client? I mean really each py file, including every script.

### A2
The script as "it is", right now, creates a "rootlib" module. There are, at least, 10 ways to do what you asked.

The easier one, using cython, would be making a "uiscriptlib" library, and re-writing the Sandbox.execfile method inside the utils.py file.

_Note: The "uiscriptlib" code has been added inside UiMain/!_

------------------------------------------
### Q3
> When I run the MakeFile_VC_Release.bat file, I get the following errors:
```
'cl' is not recognized as an internal or external command, operable program or batch file.
'lib' is not recognized as an internal or external command, operable program or batch file.
```


### A3
It's simple: it happens when the visual studio path is not specified in the %PATH% environment variable.
You have few solutions:

* Add the visual studio path in the %PATH% environment variable. (I won't suggest it)

* Add something like this at the beginning of the MakeFile_VC_Release.bat file and run it as administrator: (easy way)

```shell
call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat"
```

* You should run as admininistrator the "Visual Studio Command Prompt (2010)" and then recall the .bat from there. (highly preferable)

_Note: I've used vs2010, but it works without any problems with any visual studio version._

------------------------------------------
### Q4
> Do I really have to compile all the root files or not?
>
> I can compile a few files from the root or all files is needed?

### A4
If you use the files as "they are", only system.py and prototype.py are required.

If the module you want to include is not present in the rootlib one, the client will try to open the relative **modulename**.py file.

------------------------------------------
### Q5
> How do I fix the following error when I open the client?

> ` Error: pack_open `

### A5
Open system.py, below this:

```python
__builtins__.new_open = open
```

add:

```python
__builtins__.pack_open = open
```

------------------------------------------
### Q6
> When cythonized, is there still need dynamic linking e.g: python27.dll or library files?

### A6
Yes, the python27.dll, and the \lib folder are still required.

------------------------------------------
### Q7
> When I try to log in the game, my client crash with the following error:
```python
networkModule.SetSelectCharacterPhase - <type 'exceptions.ImportError'>:No module named uiSelectItem
```

### A7
With the default-cython code, uiSelectItem is not uiselectitem! (case-sensitive check)

On the newer root, it's typed and used in lowercase:

```shell
^\pack\root $ findstr /SC:"uiselectitem" *
interfacemodule.py:import uiselectitem
interfacemodule.py:             self.wndItemSelect = uiselectitem.SelectItemWindow()
```

You can replace uiSelectItem with uiselectitem in the interfacemodule.py.

_Note: Try to re-cythonize your files again with the last how-to-cython-mt2 version_

------------------------------------------
### Q8
> When I compile the launcher with rootlib inside, I get this error:

> `Cannot open include file 'Python.h': No such file or directory`

### A8
You haven't specified the right python path.

You have two solutions based on how your source files are written:

* You can easily copy the one used by ScriptLib into the Python<modulename>Manager.cpp file like this:

  ```cpp
  ^\Srcs\Client $ findstr /SC:"Python.h" *.h *.cpp
  ScriptLib\StdAfx.h:     #include "../../Extern/Python27/Python.h"
  ScriptLib\StdAfx.h:     #include "../../Extern/Python27/Python.h"
  UserInterface\PythonrootlibManager.cpp:#include "../../Extern/Python27/Python.h"
  ```

  Example:
  
  In `PythonrootlibManager.cpp`, replace `#include "Python.h"` with `#include "../../Extern/Python27/Python.h"`

* You can specify the right path from the project's Properties: (you should at least know what you're doing)
  ```
  From Properties, set Configuration as "All Configurations"
      and change the following values inside Configuration Properties:
  C/C++ -> General
  	  Additional Include Directories = YOURPYTHONINCLUDEPATH
  Linker -> General
      Additional Library Directories = YOURPYTHONLIBSPATH
  ```

------------------------------------------
### Q9
> When I cythonize the root files, I get warnings like these:
```
undeclared name not builtin: TRUE
undeclared name not builtin: MONETARY_UNIT0
```
> Can I solve them?

### A9
Yes, and no:

Those variables are defined by the launcher itself, and Cython can't detect what kind of "python objects" they are.

Actually, there's just a way applicable only to TRUE and FALSE:

You can gain a bit of performance if you replace TRUE with True and FALSE with False in all the **.py** files.

------------------------------------------
### Q10
> When I compile the root files, I get such an error:
```
C:\Python27\include\pyconfig.h(227): Cannot open include file: 'basetsd.h'
```
> What should I do?

### A10
You have two solutions for this:

* Following the [Q&A 3](#a3)

* Remove from C:\Python27\include\pyconfig.h the following line:
 ```cpp
 #include <basetsd.h>"
 ```

------------------------------------------
### Q11
> When I compile the launcher with rootlib inside, I get this error:

> `cannot open file `python27.lib`

(marty files only)

### A11
You have to go inside `^/Srcs/Extern/Python2/libs` and duplicate `python2.lib` to `python27.lib` (you must have both)

------------------------------------------
### Q12
> When I compile the launcher with rootlib inside, I get an error like this:
```
one or more multiply defined symbols found
"struct rootlib_SMethodDef * rootlib_init_methods" (?rootlib_init_methods@@3PAUrootlib_SMethodDef@@A) already defined in PythonrootlibManager.obj
"struct uiscriptlib_SMethodDef * uiscriptlib_init_methods" (?uiscriptlib_init_methods@@3PAUuiscriptlib_SMethodDef@@A) already defined in PythonuiscriptlibManager.obj
```

### A12
You have included the (e.g.) `PythonrootlibManager.cpp` file in the repository's project files but also included it as .cpp

Inside `^/Srcs/Client/UserInterface/UserInterface.cpp`, replace `#include "PythonrootlibManager.cpp"` with `//#include "PythonrootlibManager.cpp"` (so just comment the line).


## Intro
This repository will explain how to "convert" your root .py files to .c ones.

Actually, Cython only converts those files to pure CPython code.


## Is Cython really worth it?

- Pros
 - All the modules are compiled, and they can't be "extracted as .py" anymore.

   We can always disassemble the launcher with IDA, but the result will be pseudo-c code after waiting 6-8h of analyzing.

 - Since we're not using *.pyx files but directly *.py ones, there's no "so much optimization".

   At least, 10% of performance increasing is guaranteed.

- Cons

 - For testing purposes, it's heavy to maintain. Everytime you try to re-compile your root files, you should wait 5-10 minutes.

   You can always use the uncythonized root (.py files) when you perform tests, and compile cython whenever you will make an update in your live server.

 - The launcher's size will increase ~10mb. You can actually pack it to save space.

   If you directly use a .pyd (still 10mb), the launcher's size won't increase.


## Download

[HowToCython.zip](https://github.com/martysama0134/how-to-cython-mt2/archive/master.zip)

Such archive contains the following things:

 - Main\ -> It contains all the required files to build the rootlib.lib file

 - Main\HOW-TO-CYTHON.txt -> A complete tutorial of everything you need to do (and list of issues)

 - Extra\root\system.py -> From the official cn's root dated 2014/01/01 with the cython implementation inside

 - Extra\rootlibpyd\ -> A sample project to build your own rootlib.pyd

 - Extra\uiscriptlibpyd\ -> A sample project to build your own uiscriptlib.pyd







## FAQs

>I think you should make a guide of how to repair the errors given by the *.py files when you are cythonicing, since a lot of people don't know what to do in these cases.

The only two errors you could get when you compile your root are:

- "Decoding error, missing or incorrect coding"

  Since all the .py files are processed as korean strings, all the ones written with a different charset (arabic) will trigger this issue.

  It's explained in the .txt file, and you can simply bypass this just writing the text in the locale_game.txt file.

  You can also specify the charset to use just adding something like this at the beginning of the .py file:

  ```# -*- coding: cp1256 -*-```

  Note: cp1256 = arabic charset! (change it with the one you actually use!)

- "Expected an increase in indentation level" or similar

  This happens when the .py file has a bad tabulation, so bad written:

  It's clear that you won't be able to compile unworkable/unrunnable/broken .py files.


> Can you cythonize all the python files of the client? I mean really each py file, including every script.

The script as "it is", right now, creates a "rootlib" module. There are, at least, 10 ways to do what you asked.

The easier one, using cython, would be making a "uiscriptlib" library, and re-writing the Sandbox.execfile method inside the utils.py file.

Edit: The "uiscriptlib" will be added in the next update!

> When I run the MakeFile_VC_Release.bat file, I get the following errors:
>
> ```'cl' is not recognized as an internal or external command, operable program or batch file.
'lib' is not recognized as an internal or external command, operable program or batch file.
```

It's simple: it happens when the visual studio path is not specified in the %PATH% environment variable.
You have few solutions:

- Add the visual studio path in the %PATH% environment variable. (I won't suggest it)

- Add something like this at the beginning of the MakeFile_VC_Release.bat file and run it as administrator: (easy way)

  ``` call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat"```

- You should run as admininistrator the "Visual Studio Command Prompt (2010)" and then recall the .bat from there. (highly preferable)

Note: I've used vs2010, but it works without any problems with any vs version.

> Do I really have to compile all the root files or not?
>
> I can compile a few files from the root or all files is needed?

If you use the files as "they are", only system.py and prototype.py are required.

If the module you want to include is not present in the rootlib one, the client will try to open the relative <modulename>.py file.

> How do I fix the following error when I open the client?
>
> ```Error: pack_open```

Open system.py, below this:

``` __builtins__.new_open = open ```

add:

```__builtins__.pack_open = open```

> When cythonized, is there still need dynamic linking e.g: python27.dll or library files?

Yes, the python27.dll, and the \lib folder are still required.

> When I try to log in the game, my client crash with the following error:
>
> ```networkModule.SetSelectCharacterPhase - <type 'exceptions.ImportError'>:No module named uiSelectItem```

With the default-cython code, uiSelectItem is not uiselectitem! (case-sensitive check)

On the newer root, it's typed and used in lowercase:

```.\pack\root>findstr /SC:"uiselectitem" *
interfacemodule.py:import uiselectitem
interfacemodule.py:             self.wndItemSelect = uiselectitem.SelectItemWindow()```

You can replace uiSelectItem with uiselectitem in the interfacemodule.py.

Note: Try to re-cythonize your files again with the last how-to-cython-mt2 version

> When I compile the launcher with rootlib inside, I get this error:
>
> ```Cannot open include file 'Python.h': No such file or directory```

You haven't specified the right python path.

You have two solutions based on how your source files are written:

- You can easily copy the one used by ScriptLib into the Python<module>Manager.cpp file like this:
  ```.\Srcs\Client>findstr /SC:"Python.h" *.h *.cpp
ScriptLib\StdAfx.h:     #include "../../Extern/Python27/Python.h"
ScriptLib\StdAfx.h:     #include "../../Extern/Python27/Python.h"
UserInterface\PythonrootlibManager.cpp:#include "../../Extern/Python27/Python.h"```

- You can specify the right path from the project's Properties: (you should at least know what you're doing)
  ```From Properties, set Configuration as "All Configurations"
    and change the following values inside Configuration Properties:
C/C++ -> General
	Additional Include Directories = YOURPYTHONINCLUDEPATH
Linker -> General
	Additional Library Directories = YOURPYTHONLIBSPATH```

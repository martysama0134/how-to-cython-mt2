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
Such archive contains the following things:
 - Main\ -> It contains all the required files to build the rootlib.lib file
 - Main\HOW-TO-CYTHON.txt -> A complete tutorial of everything you need to do (and list of issues)
 - Extra\root\system.py -> From the official cn's root dated 2014/01/01 with the cython implementation inside
 - Extra\rootlibpyd\ -> A sample project to build your own rootlib.pyd
 - Extra\uiscriptlibpyd\ -> A sample project to build your own uiscriptlib.pyd


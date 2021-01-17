# not yet implemented...

import sys
sys.path.append("lib")
import utils

import os
import os.path
patternLst = []
forceRecompile = False
libname = 'rootlib'
encoding = 'cp949'
tempdir = 'cyTemp'

def printHelp():
	print "python setup.py [=f] [-oStr] [-tStr] [-eStr] files"
	print "-f : force compile option."
	print "-o[filename] : output filename.(filename.h and filename.lib)"
	print "-t[dirname] : temp dir.(If not set, then will make 'cyTemp' dir)"
	print "-e[encoding] : file encoding.(default : cp949) Each python file will have line '# -*- coding: [encoding] -*-' at the first."

for i, arg in enumerate(sys.argv[1:]):
	suffix = arg[:2]
	if "-f" == suffix:
		forceRecompile = True
	elif "-o" == suffix:
		outfilename = arg[2:]
	elif "-t" == suffix:
		tempdir = arg[2:]
	elif "-e" == suffix:
		encoding = arg[2:]
	elif "-h" == suffix:
		printHelp()
		exit(0)
	elif '-' == suffix[0]: 
		print "Unknown options."
		printHelp()
		exit(-1)
	else:
		patternLst = sys.argv[i+1:]

if [] == patternLst:
	printHelp()
	exit(-1)

matchedFiles = []
for pattern in patternLst:
	filePattern = ""
	dirPath = "."
	if -1 == pattern.rfind(os.sep):
		filePattern = pattern
	else:
		dirPath = pattern[:pattern.rfind(os.sep)]
		filePattern = pattern[pattern.rfind(os.sep):]
	
	utils.findMatchedFiles(dirPath, filePattern, matchedFiles)


def findMatchedFiles(path, pattern):
	import os
	import fnmatch
	matchedFileLst = []
	for f in os.listdir(path):
		if fnmatch.fnmatch(f, pattern):
			matchedFileLst.append(f)
	return matchedFileLst


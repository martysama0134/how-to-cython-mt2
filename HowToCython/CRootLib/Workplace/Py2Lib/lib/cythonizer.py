import utils

def run(pys, nthread = 0, outdir = "", tempdir="cyTemp", forceRecompile = False, encoding="cp949"):
	tempdir = tempdir.strip()

	if not tempdir:
		raise Exception("empty temp dir")
		return

	import sys
	import os
	realpath, _ = os.path.split(os.path.realpath(__file__))
	sys.path.insert(0, realpath + "\\..")
	from Cython.Build import cythonize
	import binascii

	if not os.path.isdir(tempdir):
		os.mkdir(tempdir)

	defineEncodingString =  '# -*- coding: ' + encoding + ' -*-'
	moduleLst = []
	
	for fn in pys:
		if fn[-3:] != ".py" and fn[-4:] != ".pyx":
			continue
		f = open(fn, "r")
		data = f.read()
		f.close()
		tempfileName = tempdir + "/" + fn
		isChanged = True
		oldCrc = 0
		newCrc = binascii.crc32(data)	
		if os.path.exists(tempfileName):
			f = open(tempfileName, "r")
			lines = f.readlines()
			try:
				oldCrc = int(lines[1][1:])
				isChanged = not(oldCrc == newCrc)
			except:
				pass

		if not forceRecompile and not isChanged:
			continue

		f = open(tempfileName, "w")
		# if encoding string already exist, receive it and not insert new encoding string.
		if -1 == data.find("-*- coding"):
			
			f.write(defineEncodingString + "\n")
		f.write("#" + str(newCrc) + "\n")
		f.write(data)
		f.write("\n")
		f.close()
		# marty: here i need to set the old mtime to the new one
		old_mtime = os.stat(fn)
		os.utime(tempfileName, (old_mtime.st_atime, old_mtime.st_mtime))
		new_mtime = os.stat(tempfileName)
		# print("old_mtime", old_mtime.st_atime, old_mtime.st_mtime)
		# print("new_mtime", new_mtime.st_atime, new_mtime.st_mtime)
		# for prototyping
		try:
			moduleLst = moduleLst + cythonize(tempfileName, nthreads=nthread)
		except Exception as e:
			os.remove(tempfileName)
			raise e

#	moduleLst = cythonize([tempdir+"/*.py", tempdir+"/*.pyx"], nthreads=nthread)
	return moduleLst
#	outfileLst = [os.path.splitext(source)[0] + ".c" for source in [m.sources for m in moduleLst]]

#	return outfileLst


from sys import path as sys_path
from os.path import splitext as op_splitext

libpath = r'..\..\..\CRootLib\Workplace\Py2Lib\lib'
sys_path.append(libpath)
rootpath = r'..\..\..\CRootLib\Workplace'
rootpath = r'.'

capNameList = {
	"logininfo":"loginInfo"
}

def checkCapName(x):
	base, ext = op_splitext(x)
	try:
		return capNameList[base.lower()] + ext
	except KeyError:
		return x

#import utils
import imp
fp, pathname, description = imp.find_module('utils', [libpath])
utils = imp.load_module('utils', fp, pathname, description)

pys = utils.findMatchedFiles(rootpath, "*.py")
if __file__ in pys:
	pys.remove(__file__)
pys = [checkCapName(x) for x in pys]

import cythonizer
moduleLst = cythonizer.run(pys, forceRecompile=True)
moduleNameLst = []
sourceFileLst = []

for m in moduleLst:
	for source in m.sources:
		base, ext = op_splitext(source)
		moduleName = base.split('/')[-1]
		moduleNameLst.append(moduleName)
		sourceFileLst.append(base + (".cpp" if "c++" == m.language else ".c"))

import sourceWriter
sourceFileName = sourceWriter.run(moduleNameLst, 'uiscriptlib')
print "%s successfully created." % sourceFileName


import sys
import app
import dbg

sys.path = []
sys.path.append("lib")

class TraceFile:
	def write(self, msg):
		dbg.Trace(msg)

class TraceErrorFile:
	def write(self, msg):
		dbg.TraceError(msg)
		dbg.RegisterExceptionString(msg)

class LogBoxFile:
	def __init__(self):
		self.stderrSave = sys.stderr
		self.msg = ""

	def __del__(self):
		self.restore()

	def restore(self):
		sys.stderr = self.stderrSave

	def write(self, msg):
		self.msg = self.msg + msg

	def show(self):
		dbg.LogBox(self.msg,"Error")

sys.stdout = TraceFile()
sys.stderr = TraceErrorFile()
#
# pack file support (must move to system.py, systemrelease.pyc)
#
import marshal
import imp
import pack
class pack_file_iterator(object):
	def __init__(self, packfile):
		self.pack_file = packfile

	def next(self):
		tmp = self.pack_file.readline()
		if tmp:
			return tmp
		raise StopIteration

_chr = __builtins__.chr

class pack_file(object):
	def __init__(self, filename, mode = 'rb'):
		assert mode in ('r', 'rb')
		if not pack.Exist(filename):
			raise IOError, 'No file or directory'
		self.data = pack.Get(filename)
		if mode == 'r':
			self.data=_chr(10).join(self.data.split(_chr(13)+_chr(10)))

	def __iter__(self):
		return pack_file_iterator(self)

	def read(self, len = None):
		if not self.data:
			return ''
		if len:
			tmp = self.data[:len]
			self.data = self.data[len:]
			return tmp
		else:
			tmp = self.data
			self.data = ''
			return tmp

	def readline(self):
		return self.read(self.data.find(_chr(10))+1)

	def readlines(self):
		return [x for x in self]

old_open = open
def open(filename, mode = 'rb'):
	if pack.Exist(filename) and mode in ('r', 'rb'):
		return pack_file(filename, mode)
	else:
		return old_open(filename, mode)

__builtins__.open = open
__builtins__.old_open = old_open
__builtins__.new_open = open

_ModuleType = type(sys)

old_import = __import__
def _process_result(code, fqname):
	# did get_code() return an actual module? (rather than a code object)
	is_module = isinstance(code, _ModuleType)

	# use the returned module, or create a new one to exec code into
	if is_module:
		module = code
	else:
		module = imp.new_module(fqname)

	# insert additional values into the module (before executing the code)
	#module.__dict__.update(values)

	# the module is almost ready... make it visible
	sys.modules[fqname] = module

	# execute the code within the module's namespace
	if not is_module:
		exec code in module.__dict__

	# fetch from sys.modules instead of returning module directly.
	# also make module's __name__ agree with fqname, in case
	# the "exec code in module.__dict__" played games on us.
	module = sys.modules[fqname]
	module.__name__ = fqname
	return module

module_do = lambda x:None
if __USE_CYTHON__:
	import rootlib

def __hybrid_import(name,globals=None,locals=None,fromlist=None, level=-1):
	if __USE_CYTHON__ and rootlib.isExist(name):
		if name in sys.modules:
			dbg.Tracen('importing from sys.modules %s' % name)
			return sys.modules[name]

		dbg.Tracen('importing from rootlib %s' % name)
		newmodule = rootlib.moduleImport(name)

		module_do(newmodule)
		sys.modules[name] = newmodule
		return newmodule
	else:
		filename = name + '.py'

		if pack.Exist(filename):
			if name in sys.modules:
				dbg.Tracen('importing from sys.modules %s' % name)
				return sys.modules[name]

			dbg.Tracen('importing from pack %s' % name)

			newmodule = _process_result(compile(pack_file(filename,'r').read(),filename,'exec'),name)

			module_do(newmodule)
			return newmodule
			#return imp.load_module(name, pack_file(filename,'r'),filename,('.py','r',imp.PY_SOURCE))
		else:
			dbg.Tracen('importing from lib %s' % name)
			return old_import(name,globals,locals,fromlist)#, level)
			#return old_import(name,globals,locals,fromlist)

def splitext(p):
	root, ext = '', ''
	for c in p:
		if c in ['/']:
			root, ext = root + ext + c, ''
		elif c == '.':
			if ext:
				root, ext = root + ext, c
			else:
				ext = c
		elif ext:
			ext = ext + c
		else:
			root = root + c
	return root, ext

def __IsCompiledFile__(sFileName):
	sBase, sExt = splitext(sFileName)
	sExt=sExt.lower()
	if sExt==".pyc" or sExt==".pyo":
		return 1
	else:
		return 0

def __LoadTextFile__(sFileName):
	sText=open(sFileName,'r').read()
	return compile(sText, sFileName, "exec")

def __LoadCompiledFile__(sFileName):
	kFile=open(sFileName)
	if kFile.read(4)!=imp.get_magic():
		raise

	kFile.read(4)

	kData=kFile.read()
	return marshal.loads(kData)

def execfile(fileName, dict):
	if __IsCompiledFile__(fileName):
		code=__LoadCompiledFile__(fileName)
	else:
		code=__LoadTextFile__(fileName)
		exec code in dict

import __builtin__
__builtin__.__import__ = __hybrid_import

# cython의 버그로... 외부 모듈의 __dict__를 수정하여, 모듈에 원래 있는 object를 수정해봐야 해당 모듈 내에서 바뀐 object가 적용되지 않는다.
#	module_do는 외부 모듈의 execfile object를 __builtin__.execfile에서 system.execfile로 치환하는 작업을 하는데 공염불이다...(외부 모듈은 __builtin__.execfile을 쓸 뿐이다.)
#	따라서 __builtin__.execfile을 system.execfile로 치환해버림...
#module_do = exec_add_module_do
__builtin__.old_execfile = __builtin__.execfile
__builtin__.execfile = execfile

"""
#
# PSYCO installation (must move to system.py, systemrelease.pyc)
#
try:
	import psyco
	#from psyco.classes import *

	def bind_me(bindable_list):
		try:
			for x in bindable_list:
				try:
					psyco.bind(x)
				except:
					pass
		except:
			pass

	_prev_psyco_old_module_do = module_do
	def module_bind(module):
		_prev_psyco_old_module_do(module)
		#print 'start binding' + str(module)
		try:
			psyco.bind(module)
		except:
			pass
		for x in module.__dict__.itervalues():
			try:
				psyco.bind(x)
			except:
				pass
		#print 'end binding'

	dbg.Trace("PSYCO installed\\n")

except Exception, msg:
	bind_me = lambda x:None
	dbg.Trace("No PSYCO support : %s\\n" % msg)
"""

def GetExceptionString(excTitle):
	(excType, excMsg, excTraceBack)=sys.exc_info()
	excText=""
	excText+=_chr(10)

	import traceback
	traceLineList=traceback.extract_tb(excTraceBack)

	for traceLine in traceLineList:
		if traceLine[3]:
			excText+="%s(line:%d) %s - %s" % (traceLine[0], traceLine[1], traceLine[2], traceLine[3])
		else:
			excText+="%s(line:%d) %s"  % (traceLine[0], traceLine[1], traceLine[2])

		excText+=_chr(10)

	excText+=_chr(10)
	excText+="%s - %s:%s" % (excTitle, excType, excMsg)
	excText+=_chr(10)

	return excText

def ShowException(excTitle):
	excText=GetExceptionString(excTitle)
	dbg.TraceError(excText)
	app.Abort()

	return 0

def RunMainScript(name):
	try:
		execfile(name, __main__.__dict__)
	except RuntimeError, msg:
		msg = str(msg)

		import localeInfo
		if localeInfo.error:
			msg = localeInfo.error.get(msg, msg)

		dbg.LogBox(msg)
		app.Abort()

	except:
		msg = GetExceptionString("Run")
		dbg.LogBox(msg)
		app.Abort()

import debugInfo
debugInfo.SetDebugMode(__DEBUG__)

loginMark = "-cs"

app.__COMMAND_LINE__ = __COMMAND_LINE__
if __USE_CYTHON__:
	#import 하는게 실행이라니... 약간ㅄ 같지만...
	import __main__
	__hybrid_import('Prototype', __main__.__dict__)
else:
	RunMainScript("prototype.py")

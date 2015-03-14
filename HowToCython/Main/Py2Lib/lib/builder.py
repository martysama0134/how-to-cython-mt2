# not yet implemented...
# -*- coding: cp949 -*-

from distutils.ccompiler import new_compiler
class Builder():
	def __init__(self, sources, plat_name = None, include_dirs = [], library_dirs = [], compiler_options = ""):
		self.sources = sources
		self.include_dirs = include_dirs
		self.library_dirs = library_dirs
		self.compiler_options = compiler_options

		if not plat_name:
			plat_name = get_platform()

		self.plat_name = plat_name

		py_include = sysconfig.get_python_inc()
		plat_py_include = sysconfig.get_python_inc(plat_specific=1)

		if not py_include in self.include_dirs:
			self.include_dirs.append(py_include)

		# Put the Python "system" include dir at the end, so that
		# any local include dirs take precedence.
		if not plat_py_include in self.include_dirs:
			self.include_dirs.append(plat_py_include)

		if os.name == 'nt':
			from distutils.msvccompiler import get_build_version
			MSVC_VERSION = int(get_build_version())
			
			# the 'libs' directory is for binary installs - we assume that
			# must be the *native* platform.  But we don't really support
			# cross-compiling via a binary install anyway, so we let it go.
			self.library_dirs.append(os.path.join(sys.exec_prefix, 'libs'))

			# Append the source distribution include and library directories,
			# this allows distutils on windows to work in the source tree
			include_dirs.append(os.path.join(sys.exec_prefix, 'PC'))
			if MSVC_VERSION == 9:
				# Use the .lib files for the correct architecture
				if plat_name == 'win32':
					suffix = ''
				else:
					# win-amd64 or win-ia64
					suffix = plat_name[4:]
				new_lib = os.path.join(sys.exec_prefix, 'PCbuild')
				if suffix:
					new_lib = os.path.join(new_lib, suffix)
				self.library_dirs.append(new_lib)

			elif MSVC_VERSION == 8:
				self.library_dirs.append(os.path.join(sys.exec_prefix,
										 'PC', 'VS8.0'))
			elif MSVC_VERSION == 7:
				self.library_dirs.append(os.path.join(sys.exec_prefix,
										 'PC', 'VS7.1'))
			else:
				self.library_dirs.append(os.path.join(sys.exec_prefix,
										 'PC', 'VC6'))
		# OS/2 (EMX) doesn't support Debug vs Release builds, but has the
		# import libraries in its "Config" subdirectory
		if os.name == 'os2':
			self.library_dirs.append(os.path.join(sys.exec_prefix, 'Config'))
			# for extensions under Cygwin and AtheOS Python's library directory must be
			# appended to library_dirs

		if sys.platform[:6] == 'cygwin' or sys.platform[:6] == 'atheos':
			if sys.executable.startswith(os.path.join(sys.exec_prefix, "bin")):
				# building third party extensions
				self.library_dirs.append(os.path.join(sys.prefix, "lib",
													  "python" + get_python_version(),
													  "config"))
			else:
				# building python standard extensions
				self.library_dirs.append('.')

	def add_sources(self, sources):
		self.sources = self.sources + sources

	def add_include_dirs(self, include_dirs):
		self.include_dirs = self.include_dirs + include_dirs

	def add_library_dirs(self, library_dirs):
		self.library_dirs = self.library_dirs +library_dirs
	
	def add_compiler_options(self, compiler_options):
		self.compiler_options = compiler_options
	
#	def run():

def run(sources, outname, debug = False, plat_name = None):
	from distutils.util import get_platform
	from distutils.core import setup
	from distutils import sysconfig
	import os
	import sys
	
	if not plat_name:
		plat_name = get_platform()
	include_dirs = []
	library_dirs = []
	py_include = sysconfig.get_python_inc()
	plat_py_include = sysconfig.get_python_inc(plat_specific=1)

	include_dirs.append(py_include)

	# Put the Python "system" include dir at the end, so that
	# any local include dirs take precedence.
	if plat_py_include != py_include:
		include_dirs.append(plat_py_include)

	if os.name == 'nt':
		from distutils.msvccompiler import get_build_version
		MSVC_VERSION = int(get_build_version())
		
		# the 'libs' directory is for binary installs - we assume that
		# must be the *native* platform.  But we don't really support
		# cross-compiling via a binary install anyway, so we let it go.
		library_dirs.append(os.path.join(sys.exec_prefix, 'libs'))

		# Append the source distribution include and library directories,
		# this allows distutils on windows to work in the source tree
		include_dirs.append(os.path.join(sys.exec_prefix, 'PC'))
		if MSVC_VERSION == 9:
			# Use the .lib files for the correct architecture
			if plat_name == 'win32':
				suffix = ''
			else:
				# win-amd64 or win-ia64
				suffix = plat_name[4:]
			new_lib = os.path.join(sys.exec_prefix, 'PCbuild')
			if suffix:
				new_lib = os.path.join(new_lib, suffix)
			library_dirs.append(new_lib)

		elif MSVC_VERSION == 8:
			library_dirs.append(os.path.join(sys.exec_prefix,
									 'PC', 'VS8.0'))
		elif MSVC_VERSION == 7:
			library_dirs.append(os.path.join(sys.exec_prefix,
									 'PC', 'VS7.1'))
		else:
			library_dirs.append(os.path.join(sys.exec_prefix,
									 'PC', 'VC6'))
	# OS/2 (EMX) doesn't support Debug vs Release builds, but has the
	# import libraries in its "Config" subdirectory
	if os.name == 'os2':
		library_dirs.append(os.path.join(sys.exec_prefix, 'Config'))
		# for extensions under Cygwin and AtheOS Python's library directory must be
		# appended to library_dirs

	if sys.platform[:6] == 'cygwin' or sys.platform[:6] == 'atheos':
		if sys.executable.startswith(os.path.join(sys.exec_prefix, "bin")):
			# building third party extensions
			library_dirs.append(os.path.join(sys.prefix, "lib",
												  "python" + get_python_version(),
												  "config"))
		else:
			# building python standard extensions
			library_dirs.append('.')
	
	script_args = ['build_clib', '--debug']#, "--plat-name="+plat_name],
	if debug:
		script_args.append('--debug')
	script_args.append('--macros=/O1')
	setup(
	  name = outname,
	  libraries = [(outname, {'sources' : sources, 'include_dirs' : include_dirs})],
	  script_args = script_args,
	)


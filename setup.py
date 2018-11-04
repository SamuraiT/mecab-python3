#!/usr/bin/env python

import os

try:
    import setuptools
except ImportError:
    pass

from distutils.core import setup, Extension
from distutils.command.build_py import build_py as _build_py

# Distutils runs build_py and then build_ext, but MeCab.py won't exist
# until build_ext runs, so subclass build_py to invoke build_ext itself.
class build_py(_build_py):
    def run(self):
        self.run_command("build_ext")
        return _build_py.run(self)

# Read a file that may or may not exist, and decode its contents as
# UTF-8, regardless of external locale settings.
def read_file(filename):
    filepath = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), filename)
    try:
        raw = open(filepath, 'rb').read()
    except OSError:
        return ''
    return raw.decode('utf-8')

def mecab_config(arg):
    return os.popen("mecab-config " + arg).readlines()[0].split()

inc_dir  = mecab_config("--inc-dir")
lib_dirs = mecab_config("--libs-only-L")
libs     = mecab_config("--libs-only-l")

swig_opts = ['-shadow', '-c++']
swig_opts.extend("-I"+d for d in inc_dir)

setup(name = "mecab-python3",
    version = '0.8.3',
    description = 'python wrapper for mecab: Morphological Analysis engine',
    long_description = read_file('README.md'),
    long_description_content_type = ”text/markdown”,
    maintainer = 'Tatsuro Yasukawa',
    maintainer_email = 't.yasukawa01@gmail.com',
    url = 'https://github.com/SamuraiT/mecab-python3',
    license = 'BSD',
    cmdclass = {"build_py": build_py},
    py_modules = ["MeCab"],
    ext_modules = [
        Extension("_MeCab",
                  ["MeCab.i"],
                  include_dirs = inc_dir,
                  library_dirs = lib_dirs,
                  libraries    = libs,
                  swig_opts    = swig_opts)
    ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

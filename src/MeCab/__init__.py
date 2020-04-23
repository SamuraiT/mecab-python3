# Second-level Python wrappers for the SWIG-generated MeCab interface.
# This file bypasses and replaces the SWIG-generated MeCab.py.
# Since we use SWIG's `-builtin` mode, it does almost nothing that we
# need, and it gets in the way of the shimming that we do need.
# Theoretically we could accomplish everything below with
# modifications to MeCab.i, but then we would have to diverge that file
# further from upstream.

from __future__ import absolute_import
from . import _MeCab

import os
import shlex

#
# Most of the public symbols come directly from the internal _MeCab
# module.
#
def _reexport_filtered(thismod, submod):
    skips = {
        # implementation details
        "Model_version", "Tagger_version", "SWIG_PyInstanceMethod_New",

        # classes exported via a wrapper
        "Tagger", "Model",
    }
    selected = []
    for sym in dir(submod):
        if sym.startswith("MECAB_") or (sym[0] != '_' and sym not in skips):
            selected.append(sym)
            setattr(thismod, sym, getattr(submod, sym))
    return selected


__all__ = _reexport_filtered(__import__(__name__), _MeCab)
del _reexport_filtered

#
# Version information
#

VERSION = _MeCab.Tagger_version()
__all__.append("VERSION")

class Tagger(_MeCab.Tagger):
    def __init__(self, args=""):
        # The first argument here isn't used . In the MeCab binary the argc and
        # argv from the shell are re-used, so the first element will be the
        # binary name.
        args = ['', '-C'] + shlex.split(args)
        # need to encode the strings to bytes, see here:
        # https://stackoverflow.com/questions/48391926/python-swig-in-typemap-does-not-work
        args = [x.encode('utf-8') for x in args]
        super(Tagger, self).__init__(args)


class Model(_MeCab.Model):
    def __init__(self, args=""):
        args = ['', '-C'] + shlex.split(args)
        args = [x.encode('utf-8') for x in args]
        super(Model, self).__init__(args)


__all__.append("Model")
__all__.append("Tagger")

# Second-level Python wrappers for the SWIG-generated MeCab interface.
# This file bypasses and replaces the SWIG-generated MeCab.py.
# Since we use SWIG's `-builtin` mode, it does almost nothing that we
# need, and it gets in the way of the shimming that we do need.
# Theoretically we could accomplish everything below with
# modifications to MeCab.i, but then we would have to diverge that file
# further from upstream.

from __future__ import absolute_import
from . import _MeCab

def _reexport_filtered(thismod, submod):
    selected = []
    for sym in dir(submod):
        if sym.startswith("MECAB_") or "_" not in sym:
            selected.append(sym)
            setattr(thismod, sym, getattr(submod, sym))
    return selected

__all__ = _reexport_filtered(__import__(__name__), _MeCab)

VERSION = _MeCab.Tagger_version()
__all__.append("VERSION")

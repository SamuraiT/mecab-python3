# Second-level Python wrappers for the SWIG-generated MeCab interface.
# This file bypasses and replaces the SWIG-generated MeCab.py.
# Since we use SWIG's `-builtin` mode, it does almost nothing that we
# need, and it gets in the way of the shimming that we do need.
# Theoretically we could accomplish everything below with
# modifications to MeCab.i, but then we would have to diverge that file
# further from upstream.

from __future__ import absolute_import
from . import _MeCab

import contextlib
import os
import tempfile

#
# Most of the public symbols come directly from the internal _MeCab
# module.
#

def _reexport_filtered(thismod, submod):
    renames = {
        "Tagger": "_Tagger",
        "Model": "_Model"
    }
    selected = []
    for sym in dir(submod):
        if sym.startswith("MECAB_") or "_" not in sym:
            rsym = renames.get(sym, sym)
            if rsym[0] != '_':
                selected.append(rsym)
            setattr(thismod, rsym, getattr(submod, sym))
    return selected

__all__ = _reexport_filtered(__import__(__name__), _MeCab)
del _reexport_filtered

#
# Version information
#

VERSION = _MeCab.Tagger_version()
__all__.append("VERSION")

#
# Detect whether or not libmecab and a dictionary have been bundled.
# If they have, pass that information down to the library when
# initializing Model and Tagger objects.
#
BUNDLED_DICDIR = None
_BUNDLED_MECABTMPL = None
def _init_bundled_info():
    pkgdatadir = os.path.dirname(__file__)
    dicdir = os.path.join(pkgdatadir, "dic")
    mecabtmpl = os.path.join(pkgdatadir, "mecabrc.in")
    if os.path.isdir(dicdir) and os.path.isfile(mecabtmpl):
        global BUNDLED_DICDIR
        global _BUNDLED_MECABTMPL
        BUNDLED_DICDIR = os.path.abspath(dicdir)
        _BUNDLED_MECABTMPL = os.path.abspath(mecabtmpl)
_init_bundled_info()
del _init_bundled_info
__all__.append("BUNDLED_DICDIR")


@contextlib.contextmanager
def _mecabrc_for_bundled_dictionary():
    dicdir = BUNDLED_DICDIR
    if dicdir is not None and "MECABRC" not in os.environ:
        mecabtmpl = _BUNDLED_MECABTMPL
        # FIXME: This will not work if the pathname BUNDLED_DICDIR
        # contains non-ASCII characters.
        with tempfile.NamedTemporaryFile(prefix="mecabrc.") as rc:
            with open(mecabtmpl, "rb") as rctmpl:
                template = rctmpl.read().decode("ascii")
            template = template.replace("@DICDIR@", dicdir)
            rc.write(template.encode("ascii"))
            rc.flush()

            os.environ["MECABRC"] = rc.name
            yield
            del os.environ["MECABRC"]
    else:
        yield


global _Model, _Tagger  # declared in _MeCab


class Tagger(_Tagger):
    def __init__(self, *args):
        with _mecabrc_for_bundled_dictionary():
            _Tagger.__init__(self, *args)

__all__.append("Tagger")


class Model(_Model):
    def __init__(self, *args):
        with _mecabrc_for_bundled_dictionary():
            _Model.__init__(self, *args)

__all__.append("Model")

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


#
# Detect whether or not libmecab and a dictionary have been bundled.
# If they have, pass that information down to the library when
# initializing Model and Tagger objects.
#
def _init_bundled_info():
    global BUNDLED_DICDIR
    global _BUNDLED_MECABTMPL
    pkgdatadir = os.path.dirname(__file__)
    dicdir = os.path.join(pkgdatadir, "dic")
    mecabtmpl = os.path.join(pkgdatadir, "mecabrc.in")
    if os.path.isdir(dicdir) and os.path.isfile(mecabtmpl):
        BUNDLED_DICDIR = os.path.abspath(dicdir)
        _BUNDLED_MECABTMPL = os.path.abspath(mecabtmpl)
    else:
        BUNDLED_DICDIR = None
        _BUNDLED_MECABTMPL = None


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
            try:
                yield
            finally:
                del os.environ["MECABRC"]
    else:
        yield


class Tagger(_MeCab.Tagger):
    def __init__(self, *args):
        with _mecabrc_for_bundled_dictionary():
            super(Tagger, self).__init__(*args)


class Model(_MeCab.Model):
    def __init__(self, *args):
        with _mecabrc_for_bundled_dictionary():
            super(Model, self).__init__(*args)


__all__.append("Model")
__all__.append("Tagger")

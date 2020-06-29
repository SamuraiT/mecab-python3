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
import sys
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


def try_import_unidic():
    """Import unidic or unidic-lite if available. Return dicdir.

    This is specifically for dictionaries installed via pip.
    """
    try:
        import unidic
        return unidic.DICDIR
    except ImportError:
        try:
            import unidic_lite
            return unidic_lite.DICDIR
        except ImportError:
            # This is OK, just give up.
            return


FAILMESSAGE = """
Failed when trying to initialize MeCab. Some things to check:

    - If you are not using a wheel, do you have mecab installed?

    - Do you have a dictionary installed? If not do this:

        pip install unidic-lite

    - If on Windows make sure you have this installed:

        https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads

    - Try creating a Model with the same arguments as your Tagger; that may
      give a more descriptive error message.

If you are still having trouble, please file an issue here:

    https://github.com/SamuraiT/mecab-python3/issues
"""


class Tagger(_MeCab.Tagger):
    def __init__(self, args=""):
        # First check for Unidic.
        unidicdir = try_import_unidic()
        if unidicdir:
            mecabrc = os.path.join(unidicdir, 'mecabrc')
            args = '-r "{}" -d "{}" '.format(mecabrc, unidicdir) + args

        # The first argument here isn't used. In the MeCab binary the argc and
        # argv from the shell are re-used, so the first element will be the
        # binary name.
        args = ['', '-C'] + shlex.split(args)

        # need to encode the strings to bytes, see here:
        # https://stackoverflow.com/questions/48391926/python-swig-in-typemap-does-not-work
        args = [x.encode('utf-8') for x in args]

        try:
            super(Tagger, self).__init__(args)
        except RuntimeError:
            sys.stderr.write(FAILMESSAGE)
            raise


class Model(_MeCab.Model):
    def __init__(self, args=""):
        # Note this is the same as the code for the Tagger.
        unidicdir = try_import_unidic()
        if unidicdir:
            mecabrc = os.path.join(unidicdir, 'mecabrc')
            args = '-r "{}" -d "{}" '.format(mecabrc, unidicdir) + args
        args = ['', '-C'] + shlex.split(args)
        args = [x.encode('utf-8') for x in args]

        try:
            super(Model, self).__init__(args)
        except RuntimeError:
            sys.stderr.write(FAILMESSAGE)
            raise


__all__.append("Model")
__all__.append("Tagger")

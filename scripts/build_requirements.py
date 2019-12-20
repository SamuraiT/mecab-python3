# This module records the version numbers and locations of various
# build requirements that may have to be downloaded and installed
# manually.

from utils import Downloadable

POOL_URL = "http://prdownloads.sourceforge.net"

SWIG = Downloadable(
    name          = "swig-4.0.1.tar.gz",
    unpacked_name = "swig-4.0.1",
    url  = POOL_URL + "/swig/swig-4.0.1.tar.gz",
    hash = "7a00b4d0d53ad97a14316135e2d702091cd5f193bb58bcfcd8bc59d41e7887a9"
)

# This module records the version numbers and locations of various
# build requirements that may have to be downloaded and installed
# manually.

from utils import Downloadable

POOL_URL = "https://deb.debian.org/debian/pool/main"

SWIG = Downloadable(
    name          = "swig-3.0.12.tar.gz",
    unpacked_name = "swig-3.0.12",
    url  = POOL_URL + "/s/swig/swig_3.0.12.orig.tar.gz",
    hash = "7cf9f447ae7ed1c51722efc45e7f14418d15d7a1e143ac9f09a668999f4fc94d"
)

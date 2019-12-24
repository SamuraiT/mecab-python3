# This module records the version numbers and locations of various
# build requirements that may have to be downloaded and installed
# manually.

from utils import Downloadable

POOL_URL = "https://src.fedoraproject.org/lookaside/pkgs"

SWIG = Downloadable(
    name          = "swig-4.0.1.tar.gz",
    unpacked_name = "swig-4.0.1",
    url = POOL_URL + "/swig/swig-4.0.1.tar.gz/sha512/"
                     "595ef01cb83adfa960ceed9c325a9429192549e8d1e9aa3ab35a"
                     "4301512a61d82e2e89a8c7939c2a5a0811254ea1832a443bd387"
                     "e11459eb2b0bafc563ad1308/swig-4.0.1.tar.gz",
    hash = "7a00b4d0d53ad97a14316135e2d702091cd5f193bb58bcfcd8bc59d41e7887a9"
)

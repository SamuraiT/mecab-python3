#! /usr/bin/env python

"""
This script is automatically invoked by setup.py if BUNDLE_LIBMECAB
is present in the environment.  It checks out a known-good version of
the libmecab source code and builds _just_ libmecab.a, so that
setup.py can then link the Python module with it.
"""

# Caution: If you change this script you may also need to change
# setup.py, as it expects to find the built library and its headers in
# a hardwired location.

# libmecab hasn't had an actual release in many years and there are no
# tags on its repository.  Le sigh.
# This rev is the most recent commit as of 2019-03-25.
LIBMECAB_REPO = "https://github.com/taku910/mecab/"
LIBMECAB_REV = "3a07c4eefaffb4e7a0690a7f4e5e0263d3ddb8a3"

LIBMECAB_DIR = "build/libmecab"

def checkout_and_build_libmecab(basedir):
    from os.path import isdir, isfile, join as p_join
    from time import sleep
    from utils import get_parallel_jobs, run, chdir, mkdir_p, touch, symlink

    if basedir:
        chdir(basedir)
    mkdir_p(LIBMECAB_DIR)

    if isdir(p_join(LIBMECAB_DIR, ".git")):
        # assume already checked out
        chdir(p_join(LIBMECAB_DIR, "mecab"))

    else:
        chdir(LIBMECAB_DIR)
        # You would think git clone would have an option to clone an
        # arbitrary <treeish>, but you would be wrong.
        run("git", "init")
        run("git", "remote", "add", "origin", LIBMECAB_REPO)
        run("git", "fetch", "origin", "--depth", "1", LIBMECAB_REV)
        run("git", "reset", "--hard", "FETCH_HEAD")
        chdir("mecab")

    if not isfile("mecab-config"):
        # Not yet configured.
        # Adjust time stamps to make sure that Make doesn't think it
        # needs to re-run autoconf or automake.
        for f in ["aclocal.m4", "config.h.in", "configure",
                  "Makefile.in", "src/Makefile.in"]:
            touch(f)
            sleep(1)

        # We build with the default charset set to UTF-8, but we don't
        # disable support for EUC-JP or Shift-JIS.
        run("./configure", "--enable-static", "--disable-shared",
            "--with-charset=utf8")

    # Override CFLAGS and CXXFLAGS to produce position-independent code,
    # even though we're only building a static library, because it will
    # be linked into a shared object (the Python extension module).
    # Only build the actual library, not the utilities.
    chdir("src")
    run("make", "-j{}".format(get_parallel_jobs()),
        "CFLAGS=-g -O2 -fPIC",
        "CXXFLAGS=-g -O2 -fPIC",
        "libmecab.la")

    # Bypass libtool.
    if not isfile("libmecab.a"):
        symlink(".libs/libmecab.a", "libmecab.a")

def main():
    from argparse import ArgumentParser
    ap = ArgumentParser(description=__doc__)
    ap.add_argument("basedir", nargs="?",
                    help="Directory in which to put {}.".format(
                        LIBMECAB_DIR))
    args = ap.parse_args()
    checkout_and_build_libmecab(args.basedir)

if __name__ == "__main__":
    main()

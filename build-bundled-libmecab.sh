#! /bin/sh

set -ex

# This script is automatically invoked by setup.py if BUNDLE_LIBMECAB
# is present in the environment.  It checks out a known-good version of
# the libmecab source code and builds _just_ libmecab.a, so that
# setup.py can then link the Python module with it. If you change this
# script you may also need to change setup.py, as it expects to find
# the built library and its headers in a hardwired location.

LIBMECAB_REPO="https://github.com/taku910/mecab/"

# libmecab hasn't had an actual release in many years and there are no
# tags on its repository.  Le sigh.
# This rev is the most recent commit as of 2018-11-13.
LIBMECAB_REV="3a07c4eefaffb4e7a0690a7f4e5e0263d3ddb8a3"

LIBMECAB_DIR="build/libmecab"

if [ ! -d "$LIBMECAB_DIR" ]; then
    mkdir -p "$LIBMECAB_DIR"
fi

# You would think git clone would have an option to clone an arbitrary
# <treeish>, but you would be wrong.
if [ ! -d "$LIBMECAB_DIR/.git" ]; then
    cd "$LIBMECAB_DIR"
    git init
    git remote add origin "$LIBMECAB_REPO"
    git fetch origin --depth 1 "$LIBMECAB_REV"
    git reset --hard FETCH_HEAD
    cd -
fi

cd "$LIBMECAB_DIR/mecab"
if [ ! -f mecab-config ]; then
    # Adjust time stamps to make sure that Make doesn't think it needs to
    # re-run autoconf or automake.
    for f in aclocal.m4 config.h.in configure Makefile.in src/Makefile.in; do
        touch $f
        sleep 1
    done

    # We build with the default charset set to UTF-8, but we don't disable
    # support for EUC-JP or Shift-JIS.
    ./configure --enable-static --disable-shared --with-charset=utf8
fi

# Override CFLAGS and CXXFLAGS to produce position-independent code,
# even though we're only building a static library, because it will
# be linked into a shared object (the Python extension module).
# Only build the actual libary, not the utilities.
cd src
make CFLAGS="-g -O2 -fPIC" CXXFLAGS="-g -O2 -fPIC" libmecab.la

# Bypass libtool.
if [ ! -e libmecab.a ]; then
    ln -s .libs/libmecab.a
fi

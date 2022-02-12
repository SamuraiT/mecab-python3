#!/bin/bash
# Install mecab, then build wheels
set -e
manylinux_version=2014
plat=x86_64

# install MeCab
# TODO specify the commit used here
git clone --depth=1 git://github.com/taku910/mecab.git
cd mecab/mecab
if [ `uname -m` == 'aarch64' ]; then
  manylinux_version=2014
  plat=aarch64
  yum -y update && yum install -y wget
  wget 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD' -O config.guess
  wget 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD' -O config.sub
fi
./configure --enable-utf8-only
make
make install

# Hack
# see here:
# https://github.com/RalfG/python-wheels-manylinux-build/issues/26
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

# Build the wheels
for PYVER in cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39 cp310-cp310; do
  # build the wheels
  /opt/python/$PYVER/bin/pip wheel /github/workspace -w /github/workspace/wheels || { echo "Failed while buiding $PYVER wheel"; exit 1; }
done

# fix the wheels (bundles libs)
for wheel in /github/workspace/wheels/*.whl; do
  auditwheel repair "$wheel" --plat manylinux${manylinux_version}_${plat} -w /github/workspace/manylinux-wheels
done

echo "Built wheels:"
ls /github/workspace/manylinux-wheels

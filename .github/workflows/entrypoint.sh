#!/bin/bash
# build wheels
set -e
manylinux_version=2014
plat=x86_64

if [ `uname -m` == 'aarch64' ]; then
  manylinux_version=2014
  plat=aarch64
fi

cd /github/workspace/mecab_$plat/mecab
make install

# Hack
# see here:
# https://github.com/RalfG/python-wheels-manylinux-build/issues/26
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

# Build the wheels
for PYVER in cp38-cp38 cp39-cp39 cp310-cp310 cp311-cp311 cp312-cp312 cp313-cp313 cp314-cp314; do
  # build the wheels
  /opt/python/$PYVER/bin/pip wheel /github/workspace -w /github/workspace/wheels || { echo "Failed while buiding $PYVER wheel"; exit 1; }
done

# fix the wheels (bundles libs)
for wheel in /github/workspace/wheels/*.whl; do
  auditwheel repair "$wheel" --plat manylinux${manylinux_version}_${plat} -w /github/workspace/manylinux-wheels
done

echo "Built wheels:"
ls /github/workspace/manylinux-wheels

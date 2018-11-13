#!/bin/bash
set -ex

yum -y update && yum -y install libtool pcre-devel curl make wget && yum clean

# Install swig
curl --location-trusted --remote-name https://downloads.sourceforge.net/project/swig/swig/swig-3.0.12/swig-3.0.12.tar.gz -o swig-3.0.12.tar.gz
tar xzf swig-3.0.12.tar.gz
pushd swig-3.0.12 && ./configure --prefix=/usr && make  && make install && popd
swig -version
rm -rf swig-3.0.12*

mkdir -p /io/dist

# Install mecab
wget "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE" -O mecab-0.996.tar.gz
tar zxfv mecab-0.996.tar.gz
pushd mecab-0.996
./configure --with-charset=utf8 --enable-utf8-only
make
make install
popd
rm -rf mecab-0.996*

# Install ipadic
wget "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM" -O mecab-ipadic-2.7.0-20070801.tar.gz
tar zxfv mecab-ipadic-2.7.0-20070801.tar.gz
pushd mecab-ipadic-2.7.0-20070801
./configure --with-charset=utf8 && make && make install && popd
rm -rf mecab-ipadic-2.7.0-20070801*

cd /io

#Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/python" setup.py bdist_wheel
done

# Bundle external shared libraries into the wheels
mkdir -p repaired_wheels/
for whl in dist/*.whl; do
    auditwheel repair "$whl" -w repaired_wheels/
done

# Install packages and test
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install mecab-python3 --no-index -f /io/repaired_wheels
    "${PYBIN}/python" -c "import MeCab"
done

# Build source
/opt/python/cp35-cp35m/bin/python setup.py sdist
rm dist/*.whl
mv repaired_wheels/*.whl /io/dist/

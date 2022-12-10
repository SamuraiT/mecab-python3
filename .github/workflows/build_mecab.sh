#!/bin/bash
# Install mecab
set -e
manylinux_version=2014
plat=x86_64

# install MeCab
git clone --depth=1 https://github.com/polm/mecab.git
if [ `uname -m` == 'aarch64' ]; then
  manylinux_version=2014
  plat=aarch64
  yum -y update && yum install -y wget
  wget 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD' -O mecab/mecab/config.guess
  wget 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD' -O mecab/mecab/config.sub
fi

mv mecab /github/workspace/mecab_$plat
cd /github/workspace/mecab_$plat/mecab/

./configure --enable-utf8-only
make

#!/bin/bash

set -ex

brew update
brew install openssl readline swig mecab mecab-ipadic
brew outdated pyenv || brew upgrade pyenv

PYTHON_VERSIONS=(2.7.15 3.4.9 3.5.6 3.6.7 3.7.1)
for PYTHON in ${PYTHON_VERSIONS[@]}; do
    pyenv install $PYTHON
    PYTHON_PATH="$(pyenv root)/versions/${PYTHON}/bin"
    "${PYTHON_PATH}/pip" install -U pip
    "${PYTHON_PATH}/pip" install -U setuptools
    "${PYTHON_PATH}/pip" install wheel
    "${PYTHON_PATH}/python" setup.py bdist_wheel
    "${PYTHON_PATH}/pip" install mecab-python3 --no-index -f dist/
    "${PYTHON_PATH}/python" -c "import MeCab"
done

ls dist/

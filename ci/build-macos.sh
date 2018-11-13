#!/bin/bash

set -ex

brew update
brew install openssl readline swig mecab mecab-ipadic
brew outdated pyenv || brew upgrade pyenv

PYTHON_VERSIONS=(2.7.15 3.4.9 3.5.6 3.6.7 3.7.1)
for PYTHON in ${PYTHON_VERSIONS[@]}; do
    pyenv install $PYTHON
    PYTHON_PATH="$(pyenv root)/versions/${PYTHON}/bin"
    ${PYTHON_PATH}/python setup.py bdist_wheel
done

$(pyenv root)/versions/${PYTHON}/bin/python setup.py sdist
ls dist/

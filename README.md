[![Current PyPI packages](https://badge.fury.io/py/mecab-python3.svg)](https://pypi.org/project/mecab-python3/)
[![Build status](https://travis-ci.org/SamuraiT/mecab-python3.svg?branch=master)](https://travis-ci.org/SamuraiT/mecab-python3)

# mecab-python3

This is a Python wrapper for the [MeCab][] morphological analyzer for Japanese
text. It works with Python 3.5 and greater, as well as Python 2.7.

(Note: Python 3.5 is not supported on OSX, see [this issue][osx-issue]). 

[MeCab]: https://taku910.github.io/mecab/
[osx-issue]: https://github.com/SamuraiT/mecab-python3/issues/41

Note that Windows wheels require a [Microsoft Visual C++
Redistributable][msvc], so be sure to install that.

[msvc]: https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads

# Basic usage

```py
>>> import MeCab
>>> wakati = MeCab.Tagger("-Owakati")
>>> wakati.parse("pythonが大好きです").split()
['python', 'が', '大好き', 'です']

>>> chasen = MeCab.Tagger("-Ochasen")
>>> print(chasen.parse("pythonが大好きです"))
python　python　　python　名詞-固有名詞-組織
が　　　ガ　　　　が　　　助詞-格助詞-一般
大好き　ダイスキ　大好き　名詞-形容動詞語幹
です　　デス　　　です　　助動詞　特殊・デス　基本形
EOS
```

The API for `mecab-python3` closely follows the API for MeCab itself,
even when this makes it not very “Pythonic.”  Please consult the [official MeCab
documentation][mecab-docs] for more information.

[mecab-docs]: https://taku910.github.io/mecab/

# Installation

Binary wheels are available for MacOS X, Linux, and Windows (64bit) are
installed by default when you use `pip`:

```sh
pip install mecab-python3
```

These wheels include an internal (statically linked) copy of the MeCab library,
but not dictionary. In order to use MeCab you'll need to install a dictionary.
`unidic-lite` is a good one to start with:

```sh
pip install unidic-lite
```

To build from source using pip,

```sh
pip install --no-binary :all: mecab-python3
```

Alternatively, you can use pip to download the source, then build it
by hand:

```sh
pip download --no-binary :all: mecab-python3
tar zxf mecab-python3-{version}.tar.gz
cd mecab-python3-{version}
python3 setup.py build
# install as you like
```

When the module is built from source, it requires the system to
provide the MeCab library and at least one dictionary.  You must have
[SWIG][], the MeCab library and headers, and a dictionary installed
before running `pip install` or `setup.py build`.  For instance, on
Debian-based Linux,

```sh
sudo apt-get install swig libmecab-dev mecab-ipadic-utf8
```

Building wheels with a bundled library and dictionary is only
supported in a sanitized CI environment.  Consult the scripts in the
`scripts` subdirectory of the source tree to see how it’s done.

[ipadic]: https://github.com/taku910/mecab/tree/master/mecab-ipadic
[SWIG]: http://www.swig.org/

# Licensing

Like MeCab itself, `mecab-python3` is copyrighted free software by
Taku Kudo <taku@chasen.org> and Nippon Telegraph and Telephone Corporation,
and is distributed under a 3-clause BSD license (see the file `BSD`).
Alternatively, it may be redistributed under the terms of the
GNU General Public License, version 2 (see the file `GPL`) or the
GNU Lesser General Public License, version 2.1 (see the file `LGPL`).

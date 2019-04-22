[![Current PyPI packages](https://badge.fury.io/py/mecab-python3.svg)](https://pypi.org/project/mecab-python3/)
[![Build status](https://travis-ci.org/SamuraiT/mecab-python3.svg?branch=master)](https://travis-ci.org/SamuraiT/mecab-python3)

# mecab-python3

This is a Python wrapper for the [MeCab][] morphological analyzer for
Japanese text.  It works with Python 3.4 and greater, as well as
Python 2.7.

[MeCab]: https://taku910.github.io/mecab/

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
even when this makes it not very “Pythonic.”  Please consult the MeCab
documentation for more information.

# Installation

Binary wheels are available for MacOS X and Linux, and are installed
by default when you use `pip`:

```sh
pip install mecab-python3
```

These wheels include an internal (statically linked) copy of the MeCab
library, and a copy of the [`mecab-ipadic`][ipadic] dictionary (using
UTF-8 text encoding), which is automatically used by default.  If you
wish to use a different dictionary, you will need to install it
yourself, write a `mecabrc` file directing MeCab to use it, and set
the environment variable `MECABRC` to point to this file.

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

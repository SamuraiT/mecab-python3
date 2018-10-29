[![Build Status](https://travis-ci.org/klauer/mecab-python3.svg?branch=master)](https://travis-ci.org/klauer/mecab-python3)

mecab-python3
-------------

This python wrapper for mecab works on both **python3.x** and **python2.x**.


Installation and Usage
--------------

```
pip install mecab-python3
```

You must have `mecab` and `swig` installed before running `setup.py`.
For instance, on Debian-based Linux,

```
sudo apt-get install mecab mecab-ipadic-utf8 libmecab-dev swig
```

2. How to use?

   see 'test.py' as a sample program.

3. Simple example

```
import MeCab
mecab = MeCab.Tagger ("-Ochasen")
print(mecab.parse("pythonが大好きです"))
```


License
-------
MeCab is copyrighted free software by Taku Kudo <taku@chasen.org> and
Nippon Telegraph and Telephone Corporation, and is released under
any of the GPL (see the file GPL), the LGPL (see the file LGPL), or the
BSD License (see the file BSD).

mecab-python3
-------------
This is the python3 versioin of mecab.


Installtion and Usage
--------------
1. Installation

```
pip install mecab-python3
```

Before installing mecabpython3, make sure you have installed *`mecab`*
already.

example of installtion.
Assume you are using Debian-based linux.

```
sudo apt-get install libmecab-dev
sudo apt-get install mecab mecab-ipadic-utf8
pip install mecab-python3
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

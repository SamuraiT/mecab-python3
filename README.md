mecab-python3
-------------
This is the python3 versioin of mecab.



License
-------
MeCab is copyrighted free software by Taku Kudo <taku@chasen.org> and
Nippon Telegraph and Telephone Corporation, and is released under
any of the GPL (see the file GPL), the LGPL (see the file LGPL), or the
BSD License (see the file BSD).




MeCab python module
--------------
$Id: README,v 1.1.1.1 2005/12/03 14:18:50 taku-ku Exp $;

1. Installation

```
pip install git+https://github.com/SamuraiT/mecab-python3
```


2. How to use?

   see 'test.py' as a sample program.

3. Simple example

```
import MeCab
mecab = MeCab.Tagger ("-Ochasen")
print(mecab.parse ("pythonが大好きです"))
```

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Minimal test of MeCab functionality.

import contextlib
import sys
import unittest

import MeCab


# TODO: More test sentences.
SENTENCE = "太郎はこの本を二郎を見た女性に渡した。"

SENTENCES = (
    ("すももももももももの内", "すもも も もも も もも の 内".split()),
    ("吾輩は猫である。", "吾輩 は 猫 で ある 。".split()),
    ("ははははは丈夫だ", "はははは は 丈夫 だ".split()),
    ("カムパネルラが手をあげました。", "カムパネルラ が 手 を あげ まし た 。".split()),
    ("コミックマーケットは同人誌を中心にしてすべての表現者を受け入れ、"
     "継続することを目的とした表現の可能性を拡げるための「場」である",
     "コミック マーケット は 同人 誌 を 中心 に し て すべて の 表現 者 を 受け入れ 、 "
     "継続 する こと を 目的 と し た 表現 の 可能 性 を 拡げる ため の 「 場 」 で ある"
     .split())
)

# BUG: If we instantiate a new tagger for each test case, then the
# second and subsequent tagger instantiations will produce garbage.
# I suspect this is a bug somewhere within libmecab itself.
TAGGER = MeCab.Tagger()

# Check if we are using Unidic and only test in that case. In particular this
# uses only unidic-lite since there are different versions of Unidic.
USING_UNIDIC = False
try:
    import unidic_lite   # noqa: F401
    USING_UNIDIC = True
except ImportError:
    pass


# unittest.TestCase.subTest is only available in python >=3.5, not 2.x
# provide a shim
if hasattr(unittest.TestCase, 'subTest'):
    def sub_test(testcase, *args, **kwargs):
        return testcase.subTest(*args, **kwargs)
else:
    @contextlib.contextmanager
    def sub_test(testcase, *args, **kwargs):
        yield


class TestTagger(unittest.TestCase):
    def setUp(self):
        self.tagger = TAGGER

    def test_metadata(self):
        sys.stdout.write("# Testing MeCab version {}\n".format(MeCab.VERSION))

        d = self.tagger.dictionary_info()
        if not d:
            sys.stdout.write("# No dictionaries found.\n")
            return

        n = 1
        while d:
            sys.stdout.write("# Dictionary #{}:\n"
                             "#    filename: {}\n"
                             "#     version: {}\n"
                             "#     charset: {}\n"
                             "#        type: {}\n"
                             "#        size: {}\n"
                             "#       lsize: {}\n"
                             "#       rsize: {}\n"
                             .format(n, d.filename, d.version, d.charset,
                                     d.type, d.size, d.lsize, d.rsize))
            n += 1
            d = d.next

    # The segmentation of the test sentence could vary depending on
    # the dictionaries available, so we can't test for a specific
    # result.  However, parse() and parseToNode() should always
    # produce a sequence of nodes whose "surface"s do not overlap
    # and which add back up to be the entire sentence.  (This will,
    # for instance, detect a regression of
    # https://github.com/SamuraiT/mecab-python3/issues/19 .)

    # XXX The above is not strictly true - "surface" does not include some
    # kinds of whitespace. If your input is "hello how are you" there will be
    # no white space in the surfaces. It seems the only way to tell if there
    # was a space from the C api is to check if rlength is longer than length
    # for a node, in which case there was a space before it.

    def tokenize(self, sentence):
        parsed = self.tagger.parse(sentence)
        nodes = []
        last = False
        for line in parsed.splitlines():
            if line == "EOS":
                last = True
                continue
            self.assertFalse(last)
            surface, feature = line.strip().split("\t", 1)
            nodes.append((surface, feature))
        self.assertTrue(last)
        return nodes

    def test_parse(self):
        nodes = self.tokenize(SENTENCE)
        self.validateNodes(SENTENCE, nodes)

    def test_parseToNode(self):
        m = self.tagger.parseToNode(SENTENCE)
        nodes = []
        while m:
            nodes.append((m.surface, m.feature))
            m = m.next
        self.validateNodes(SENTENCE, nodes)

    @unittest.skipIf(not USING_UNIDIC, "Not using unidic")
    def test_tokenization(self):
        for sentence, answer in SENTENCES:
            tokens = [tok[0] for tok in self.tokenize(sentence)]
            with sub_test(self, sentence=sentence):
                self.assertEqual(tokens, answer)

    def validateNodes(self, sentence, nodes):
        for surface, feature in nodes:
            n = len(surface)
            self.assertTrue(len(sentence) >= n)
            self.assertEqual(surface, sentence[:n])
            sentence = sentence[n:]
        self.assertEqual(sentence, u"")

    # TODO: "Lattice" mode output is much more complicated and I don't
    # understand it well enough to write tests for it.  For now, just
    # make sure that parsing a lattice doesn't crash or throw an
    # exception.
    def test_parseToLattice(self):
        lattice = MeCab.Lattice()
        lattice.set_sentence(SENTENCE)
        self.tagger.parse(lattice)

        # len = lattice.size()
        # for i in range(len + 1):
        #     b = lattice.begin_nodes(i)
        #     e = lattice.end_nodes(i)
        #     while b:
        #         print("B[%d] %s\t%s" % (i, b.surface, b.feature))
        #         b = b.bnext
        #     while e:
        #         print("E[%d] %s\t%s" % (i, e.surface, e.feature))
        #         e = e.bnext
        # print("EOS");


if __name__ == "__main__":
    unittest.main()

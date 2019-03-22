#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Minimal test of MeCab functionality.

import os
import sys
import unittest

import MeCab

# TODO: More test sentences.
SENTENCE = "太郎はこの本を二郎を見た女性に渡した。"

# BUG: If we instantiate a new tagger for each test case, then the
# second and subsequent tagger instantiations will produce garbage.
# I suspect this is a bug somewhere within libmecab itself.
TAGGER = MeCab.Tagger(os.environ.get("MECAB_TAGGER_ARGS", ""))

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

    def test_parse(self):
        parsed = self.tagger.parse(SENTENCE)
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
        self.validateNodes(SENTENCE, nodes)

    def test_parseToNode(self):
        m = self.tagger.parseToNode(SENTENCE)
        nodes = []
        while m:
            nodes.append((m.surface, m.feature))
            m = m.next
        self.validateNodes(SENTENCE, nodes)

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

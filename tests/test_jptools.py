# -*- coding: utf8 -*-
# test_jptools.py
# Test the Japanese NLP tools
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from feet.entities.jptools import JAParser
import unittest


class JAParserTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_singleton(self):
        self.assertEqual(JAParser(), JAParser())
        self.assertEqual(JAParser().mecab, JAParser().mecab)

    def test_word_tokenize_text_is_none(self):
        self.assertEqual(JAParser().word_tokenize(None), None)

    def test_word_tokenize_without_separators(self):
        text = 'これは日本語です。'
        self.assertEqual(JAParser().word_tokenize(text, False),
                         ['これ', 'は', '日本語', 'です'])

    def test_word_tokenize_with_separators(self):
        text = 'これは日本語です。'
        self.assertEqual(JAParser().word_tokenize(text, True),
                         ['これ', 'は', '日本語', 'です', '。'])

    def test_sent_tokenize_text_is_none(self):
        self.assertEqual(JAParser().sent_tokenize(None), [])

    def test_sent_tokenize_text(self):
        text = 'これは日本語です。これは私の最高の例です。'
        self.assertEqual(JAParser().sent_tokenize(text),
                         [
                         'これは日本語です',
                         'これは私の最高の例です'
                         ])

    def test_extract_entities(self):
        text = '国際連合は、国際連合憲章の下、1945年に設立された国際組織である'
        entities = JAParser().extract_entities(text, True)
        self.assertIn('国際連合', entities)


if __name__ == '__main__':
    unittest.main()

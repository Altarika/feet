# -*- coding: utf8 -*-
# test_nlp.py
# Test the feet.entities.nlp module
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from feet.entities.nlp import Parser
import unittest


class GetLanguageTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_language_text_is_none(self):
        self.assertEqual(Parser().detect_language(None), None)

    def test_language_english(self):
        text = 'This is my best example'
        self.assertEqual(Parser().detect_language(text), 'en')

    def test_language_french(self):
        text = 'Ceci est mon meilleur exemple'
        self.assertEqual(Parser().detect_language(text), 'fr')

    def test_language_japanese(self):
        text = 'これは日本語です'
        self.assertEqual(Parser().detect_language(text), 'ja')

    def test_language_spanish(self):
        text = 'Este es mi mejor ejemplo'
        self.assertEqual(Parser().detect_language(text), 'es')

    def test_language_german(self):
        text = 'Das ist mein bestes Beispiel'
        self.assertEqual(Parser().detect_language(text), 'de')

    def test_language_italian(self):
        text = 'Questo è il mio miglior esempio'
        self.assertEqual(Parser().detect_language(text), 'it')

    def test_language_simplified_chinese(self):
        text = '这是我最好的例子'
        self.assertEqual(Parser().detect_language(text), 'zh-cn')

    def test_language_traditional_chinese(self):
        text = '這是我最好的例子'
        self.assertEqual(Parser().detect_language(text), 'zh-cn')

    def test_language_korean(self):
        text = '이것이 나의 가장 좋은 본보기이다'
        self.assertEqual(Parser().detect_language(text), 'ko')

    def test_tokenize_text_is_none(self):
        self.assertEqual(Parser().tokenize(None)[0], [])

    def test_tokenize_english(self):
        text = 'This is my best example.'
        self.assertEqual(Parser().tokenize(text)[0],
                         [['This', 'is', 'my', 'best', 'example', '.']])

    def test_tokenize_japanese(self):
        text = 'これは日本語です。これは私の最高の例です。'
        self.assertEqual(Parser().tokenize(text, 'ja')[0],
                         [
                         ['これ', 'は', '日本語', 'です'],
                         ['これ', 'は', '私', 'の', '最高', 'の', '例', 'です']
                         ])


if __name__ == '__main__':
    unittest.main()

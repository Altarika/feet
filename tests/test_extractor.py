# -*- coding: utf8 -*-
# test_extractor.py
# Test the feet.entities.extractor module
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import os
import unittest
import inspect
from feet.entities.extractor import Extractor
from feet.entities.dictionary import CSVDictionary
from feet.entities.registry import Registry

PATH = os.path.dirname(os.path.abspath(__file__))
EVENTS_FILE = os.path.join(PATH, 'test_data/events_ja.txt')
COUNTRIES_FILE = os.path.join(PATH, 'test_data/countries_en.csv')
CITIES_FILE = os.path.join(PATH, 'test_data/world-cities.csv')
ENGLISH_TEXT = os.path.join(PATH, 'test_data/english_text_long.txt')


class ExtractorTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        Registry.flush('ExtractorTests')

    def test_extract_sentence(self):
        """
        Test extracting entities from a sentence in English
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           dict_class=CSVDictionary,
                                           key_prefix='ExtractorTests')
        countries = registry.get_dict('countries')
        countries.load_file(COUNTRIES_FILE, 'en')
        text = "I want to buy flight tickets for Japan"
        engine = Extractor(countries)
        results = engine.extract(text, 'en')
        terms = []
        for element in results[0]:
            if element['entity_found'] == 1:
                terms = list(set(terms).union(element['entity_candidates']))
        self.assertIn('Japan', terms)

    def test_extract_document(self):
        """
        Test extracting cities from a Wikipedia article that describes the UN.
        This is a very good example to show problems of ambiguities in selecting
        entities: e.g. Venezuela is both a country and a city, liberty is a
        city and a concept, Roosevelt is a man and a city etc.
        Conclusion: We mostly have a problem of noise in the results not silence
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           dict_class=CSVDictionary,
                                           key_prefix='ExtractorTests')
        cities = registry.get_dict('cities')
        cities.load_file(CITIES_FILE, 'en')
        text = open(ENGLISH_TEXT).read()
        engine = Extractor(cities)
        results = engine.extract(text, 'en')
        terms = []
        for element in results[0]:
            if element['entity_found'] == 1:
                terms = list(set(terms).union(element['entity_candidates']))
        self.assertIn('Nairobi', terms)

    def test_extract_jp_sentence(self):
        """
        Test extracting entities from text in Japanase
        """
        test_sentence_jp = u'[TOMMY HILFIGER]3階「TOMMY HILFIGER」\
リニューアルオープン！ 6月2日より3階Plaza South「TOMMY HILFIGER」\
がリニューアルオープン！ https://t.co/Nf3GTF0OQD #Lazona'
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='ExtractorTests')
        events = registry.get_dict('events')
        events.load_file(EVENTS_FILE, 'ja')
        engine = Extractor(events)
        results = engine.extract(test_sentence_jp.encode('utf8'), 'ja')
        terms = []
        for element in results[0]:
            if element['entity_found'] == 1:
                terms = list(set(terms).union(element['entity_candidates']))
        self.assertIn('リニューアルオープン', terms)


if __name__ == '__main__':
    unittest.main()

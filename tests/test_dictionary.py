# -*- coding: utf8 -*-
# test_dictionary.py
# Test the feet.entities.dictionary module
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import os
import inspect
import unittest
from feet.entities.dictionary import Dictionary, CSVDictionary
from feet.entities.registry import Registry

PATH = os.path.dirname(os.path.abspath(__file__))
EVENTS_FILE = os.path.join(PATH, 'test_data/events_ja.txt')
COUNTRIES_FILE = os.path.join(PATH, 'test_data/countries_en.csv')


class DictionaryTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        Registry.flush('DictionaryTests')

    def test_reset_dictionary(self):
        """
        Test reset of one entity dictionary
        """
        countries_db = CSVDictionary(
            inspect.stack()[0][3],
            key_prefix='DictionaryTests')
        self.assertEqual(countries_db.load_list(['test', 'test2'], 'en'), 2)
        self.assertTrue(countries_db.delete())
        self.assertEqual(countries_db.languages(), [])
        self.assertEqual(countries_db.cardinality('en'), 0)

    def test_initialize_from_csv_file(self):
        """
        Test initialize dictionary from csv file
        """
        countries_db = CSVDictionary(
            inspect.stack()[0][3],
            key_prefix='DictionaryTests')
        self.assertEqual(countries_db.load_file(COUNTRIES_FILE, 'en'), 249)

    def test_initialize_from_text_file(self):
        """
        Test loading of terms from a text file
        """
        events_db = Dictionary(
            inspect.stack()[0][3],
            key_prefix='DictionaryTests')
        self.assertEqual(events_db.load_file(EVENTS_FILE, 'ja'), 40)
        self.assertTrue('ja' in events_db.languages())
        self.assertEqual(events_db.cardinality('ja'), 40)

    def test_adding_terms(self):
        """
        Test retrieving list of all entities in a dictionary
        """
        cities_db = Dictionary(
            inspect.stack()[0][3],
            key_prefix='DictionaryTests')
        self.assertEqual(cities_db.load_list(['Paris', 'Tokyo'], 'en'), 2)
        self.assertTrue('en' in cities_db.languages())
        self.assertEqual(cities_db.cardinality('en'), 2)
        self.assertTrue(cities_db.add_term('New York', 'en'))
        self.assertEqual(cities_db.cardinality('en'), 3)
        self.assertItemsEqual(cities_db.terms('en'), ['Paris', 'Tokyo',
                                                      'New York'])
        self.assertEqual(cities_db.exact_match('New York', 'en'), 1)
        self.assertItemsEqual(cities_db.candidates('new', 'en'), ['new york'])
        self.assertTrue(cities_db.add_term('New Orleans', 'en'))
        self.assertEqual(cities_db.cardinality('en'), 4)
        self.assertItemsEqual(cities_db.terms('en'), ['Paris', 'Tokyo',
                                                      'New York',
                                                      'New Orleans'])
        self.assertEqual(cities_db.exact_match('New Orleans', 'en'), 1)
        self.assertItemsEqual(cities_db.candidates('new', 'en'),
                              ['new york', 'new orleans'])

    def test_retrieving_terms(self):
        """
        Test retrieving list of all entities in a dictionary
        """
        cities_db = Dictionary(
            inspect.stack()[0][3],
            key_prefix='DictionaryTests')
        self.assertEqual(cities_db.load_list(['Apple', 'Orange'], 'en'), 2)
        self.assertTrue('en' in cities_db.languages())
        self.assertEqual(cities_db.cardinality('en'), 2)
        self.assertItemsEqual(cities_db.terms('en'), ['Apple', 'Orange'])

    def test_deleting_terms(self):
        """
        Test retrieving list of all entities in a dictionary
        """
        cities_db = Dictionary(
            inspect.stack()[0][3],
            key_prefix='DictionaryTests')
        self.assertEqual(cities_db.load_list(['Paris', 'Tokyo'], 'en'), 2)
        self.assertTrue('en' in cities_db.languages())
        self.assertEqual(cities_db.cardinality('en'), 2)
        self.assertTrue(cities_db.delete_term('Paris', 'en'))
        self.assertEqual(cities_db.cardinality('en'), 1)
        self.assertItemsEqual(cities_db.terms('en'), ['Tokyo'])
        self.assertEqual(cities_db.exact_match('Paris', 'en'), 0)
        self.assertTrue(cities_db.delete_term('Tokyo', 'en'))
        self.assertEqual(cities_db.cardinality('en'), 0)
        self.assertItemsEqual(cities_db.terms('en'), [])
        self.assertEqual(cities_db.exact_match('Tokyo', 'en'), 0)

    def test_deleting_unknown_term(self):
        """
        Test retrieving list of all entities in a dictionary
        """
        cities_db = Dictionary(
            inspect.stack()[0][3],
            key_prefix='DictionaryTests')
        self.assertEqual(cities_db.load_list(['Paris', 'Tokyo'], 'en'), 2)
        self.assertTrue('en' in cities_db.languages())
        self.assertEqual(cities_db.cardinality('en'), 2)
        self.assertEqual(cities_db.delete_term('Paris', 'en'), 1)
        self.assertEqual(cities_db.cardinality('en'), 1)
        self.assertItemsEqual(cities_db.terms('en'), ['Tokyo'])
        self.assertEqual(cities_db.exact_match('Paris', 'en'), 0)

    def test_paging_terms(self):
        """
        Test retrieving list of all entities in a dictionary
        """
        countries_db = CSVDictionary(
            inspect.stack()[0][3],
            key_prefix='DictionaryTests')
        self.assertEqual(countries_db.load_file(COUNTRIES_FILE, 'en'), 249)
        self.assertTrue('en' in countries_db.languages())
        self.assertEqual(countries_db.cardinality('en'), 249)
        self.assertItemsEqual(countries_db.terms('en', 0, 5),
                              ['Afghanistan', 'Åland Islands',
                               'Albania', 'Algeria', 'American Samoa'])
        self.assertItemsEqual(countries_db.terms('en', 1, 5),
                              ['Andorra', 'Angola',
                               'Anguilla', 'Antarctica',
                               'Antigua and Barbuda'])


if __name__ == '__main__':
    unittest.main()

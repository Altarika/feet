# -*- coding: utf8 -*-
# test_registry.py
# Test the feet.entities.registry module
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import unittest
import inspect
from feet.entities.registry import Registry
from feet.entities.dictionary import Dictionary


class RegistryTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        Registry.flush('RegistryTests')

    def test_no_registries(self):
        """
        Test get registries from empty prefix
        """
        registries = Registry.list(inspect.stack()[0][3])
        self.assertEqual(registries, [])

    def test_add_registry(self):
        """
        Test add registry
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='RegistryTests')
        self.assertIsInstance(registry, Registry)
        registries = Registry.list('RegistryTests')
        self.assertIn(inspect.stack()[0][3], registries)

    def test_find_registry(self):
        """
        Test find registry
        """
        Registry.find_or_create(inspect.stack()[0][3],
                                key_prefix='RegistryTests')
        Registry.find_or_create(inspect.stack()[0][3],
                                key_prefix='RegistryTests')
        registries = Registry.list('RegistryTests')
        self.assertIn(inspect.stack()[0][3], registries)

    def test_delete_registry(self):
        """
        Test delete a registry
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='RegistryTests')
        registry.delete()
        registries = Registry.list('RegistryTests')
        self.assertNotIn(inspect.stack()[0][3], registries)

    def test_reset_registry(self):
        """
        Test reset a registry
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='RegistryTests')
        self.assertIsInstance(registry.get_dict('countries'), Dictionary)
        self.assertTrue(registry.reset())
        self.assertEqual(registry.list(), [])

    def test_add_dictionary(self):
        """
        Test add a dictionary into the registry
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='RegistryTests')
        entity = registry.get_dict('countries')
        self.assertIsInstance(entity, Dictionary)
        self.assertIn('countries', registry.dictionaries())

    def test_find_dictionary(self):
        """
        Test find a dictionary from registry
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='RegistryTests')
        registry.get_dict('countries')
        entity_dictionary = registry.get_dict('countries')
        self.assertIsInstance(entity_dictionary, Dictionary)

    def test_list_dictionaries_empty(self):
        """
        Test list of dictionaries is emnpty
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='RegistryTests')
        self.assertEqual(registry.list(), [])
        self.assertFalse(registry.reset())

    def test_list_dictionaries(self):
        """
        Test get the list of dictionaries from a registry
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='RegistryTests')
        registry.get_dict('countries')
        registry.get_dict('cities')
        registry.get_dict('events')
        self.assertItemsEqual(registry.dictionaries(),
                              ['countries', 'cities', 'events'])

    def test_delete_dictionary(self):
        """
        Test delete a dictionary from the registry
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='RegistryTests')
        registry.get_dict('countries')
        registry.get_dict('cities')
        registry.get_dict('events')
        self.assertTrue(registry.del_dict('countries'))
        self.assertNotIn('countries', registry.dictionaries())

    def test_delete_unknown_dictionary(self):
        """
        Test delete an unknown dictionary from the registry
        """
        registry = Registry.find_or_create(inspect.stack()[0][3],
                                           key_prefix='RegistryTests')
        registry.get_dict('countries')
        registry.get_dict('cities')
        self.assertFalse(registry.del_dict('events'))


if __name__ == '__main__':
    unittest.main()

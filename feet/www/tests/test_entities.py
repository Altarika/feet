# -*- coding: utf8 -*-
# test_entities.py
# Test the api endpoints
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import os
import csv
import unittest
import inspect
import json
from tornado.testing import AsyncHTTPTestCase
from feet.www.urls import make_app
from feet.utils.logger import LoggingMixin
from feet.entities.registry import Registry

PATH = os.path.dirname(os.path.abspath(__file__))
COUNTRIES_FILE = os.path.join(PATH, '../../../tests/test_data/countries_en.csv')


# parse test data csv files, quick and dirty
def parse_csv_file(path):
    first_line = True
    with open(path, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if first_line:
                first_line = False
                continue
            else:
                yield row[0]


class GenericTestCase(LoggingMixin, AsyncHTTPTestCase):
    def get_app(self):
        return make_app()


class SmokeTest(GenericTestCase):
    def test_http_fetch(self):
        """
        Smoke test
        """
        response = self.fetch('/')
        self.assertEqual(response.code, 200)


class RegistryAPITest(GenericTestCase):
    def tearDown(self):
        Registry.flush('registry_api_test')
        super(AsyncHTTPTestCase, self).tearDown()

    def test_get_list_of_registries_empty(self):
        """
        Test get empty list of registries
        """
        response = self.fetch(
            '/database/0/prefix/registry_api_test/registries/')
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['registries'], [])

    def test_add_get_registry(self):
        """
        Test add a registry and get registry entities
        """
        response = self.fetch(
            '/database/0/prefix/registry_api_test/registries/{}/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        response = self.fetch(
            '/database/0/prefix/registry_api_test/registries/')
        self.assertEqual(json.loads(response.body)['registries'],
                         [inspect.stack()[0][3]])
        response = self.fetch(
            '/database/0/prefix/registry_api_test/registries/{}/'
            .format(inspect.stack()[0][3]))
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['entities'], [])

    def test_delete_registry(self):
        """
        Test delete a registry
        """
        response = self.fetch(
            '/database/0/prefix/registry_api_test/registries/{}/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        response = self.fetch(
            '/database/0/prefix/registry_api_test/registries/{}/'
            .format(inspect.stack()[0][3]),
            method='DELETE')
        self.assertEqual(response.code, 200)
        response = self.fetch(
            '/database/0/prefix/registry_api_test/registries/')
        self.assertEqual(json.loads(response.body)['registries'], [])


class EntityAPITest(GenericTestCase):
    def tearDown(self):
        Registry.flush('entity_api_test')
        super(AsyncHTTPTestCase, self).tearDown()

    def test_add_get_entity(self):
        """
        Test add a registry and get registry entities
        """
        response = self.fetch(
            '/database/0/prefix/entity_api_test/registries/{}/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        response = self.fetch(
            '/database/0/prefix/entity_api_test/registries/{}/entities/test/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        response = self.fetch(
            '/database/0/prefix/entity_api_test/registries/{}/'
            .format(inspect.stack()[0][3]))
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['entities'], ['test'])
        response = self.fetch(
            '/database/0/prefix/entity_api_test/registries/{}/entities/test/'
            .format(inspect.stack()[0][3]))
        self.assertEqual(json.loads(response.body)['languages'], [])

    def test_add_delete_entity(self):
        """
        Test add a registry and get registry entities
        """
        response = self.fetch(
            '/database/0/prefix/entity_api_test/registries/{}/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        response = self.fetch(
            '/database/0/prefix/entity_api_test/registries/{}/entities/test/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        response = self.fetch(
            '/database/0/prefix/entity_api_test/registries/{}/entities/test/'
            .format(inspect.stack()[0][3]),
            method='DELETE')
        self.assertEqual(response.code, 200)
        response = self.fetch(
            '/database/0/prefix/entity_api_test/registries/{}/'
            .format(inspect.stack()[0][3]))
        self.assertEqual(json.loads(response.body)['entities'], [])


class LanguageAPITest(GenericTestCase):
    def tearDown(self):
        Registry.flush('language_api_test')
        super(AsyncHTTPTestCase, self).tearDown()

    def test_add_get_delete_language(self):
        """
        Test add, get and delete a language
        """
        response = self.fetch(
            '/database/0/prefix/language_api_test/registries/{}/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # add entity
        response = self.fetch(
            '/database/0/prefix/language_api_test/registries/{}/entities/test/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # add entity language
        response = self.fetch(
            '/database/0/prefix/language_api_test/registries/' +
            '{}/entities/test/lang/en/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # list entity languages
        response = self.fetch(
            '/database/0/prefix/language_api_test/registries/{}/entities/test/'
            .format(inspect.stack()[0][3]))
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertItemsEqual(['en'], json_response['languages'])
        # delete entity language
        response = self.fetch(
            '/database/0/prefix/language_api_test/registries/' +
            '{}/entities/test/lang/en/'
            .format(inspect.stack()[0][3]),
            method='DELETE')
        self.assertEqual(response.code, 200)
        # list entity languages
        response = self.fetch(
            '/database/0/prefix/language_api_test/registries/{}/entities/test/'
            .format(inspect.stack()[0][3]))
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertEqual([], json_response['languages'])


class TermsAPITest(GenericTestCase):
    def tearDown(self):
        Registry.flush('terms_api_test')
        super(AsyncHTTPTestCase, self).tearDown()

    def test_add_list_delete_terms(self):
        """
        Test add, list and delete terms
        """
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/{}/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # add entity
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/{}/entities/test/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # add entity language
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/test/lang/en/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # add terms
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/test/lang/en/terms/'
            .format(inspect.stack()[0][3]),
            method='POST',
            body='{"terms":["Paris","Tokyo"]}')
        self.assertEqual(response.code, 200)
        # list terms
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/test/lang/en/terms/'
            .format(inspect.stack()[0][3]))
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertItemsEqual(['Tokyo', 'Paris'], json_response['terms'])
        # delete terms
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/test/lang/en/terms/Tokyo/'
            .format(inspect.stack()[0][3]),
            method='DELETE')
        self.assertEqual(response.code, 200)
        # list terms
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/test/lang/en/terms/'
            .format(inspect.stack()[0][3]))
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertItemsEqual(['Paris'], json_response['terms'])


class EntityExtractTestCase(GenericTestCase):
    def tearDown(self):
        Registry.flush('extract_api_test')
        super(AsyncHTTPTestCase, self).tearDown()

    def test_extract_terms_from_text(self):
        """
        Test extract with predefined grammar
        """
        response = self.fetch(
            '/database/0/prefix/extract_api_test/registries/{}/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # add entity
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/{}/entities/country/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # add entity language
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/country/lang/en/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)

        # add terms
        for term in parse_csv_file(COUNTRIES_FILE):
            response = self.fetch(
                '/database/0/prefix/terms_api_test/registries/' +
                '{}/entities/country/lang/en/terms/'
                .format(inspect.stack()[0][3]),
                method='POST',
                body=json.dumps({"terms": [term]}))
            self.assertEqual(response.code, 200)

        # check cardinality
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/country/lang/en/'
            .format(inspect.stack()[0][3]))
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['count'], 249)

        # list entity terms
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/country/lang/en/terms/'
            .format(inspect.stack()[0][3]) +
            '?page=0&count=5')
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertItemsEqual([u'Afghanistan', u'Åland Islands',
                               u'Albania', u'Algeria', u'American Samoa'],
                              json_response['terms'])

        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/country/lang/en/terms/'
            .format(inspect.stack()[0][3]) +
            '?page=1&count=5')
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertItemsEqual([u'Andorra', u'Angola',
                               u'Anguilla', u'Antarctica',
                               u'Antigua and Barbuda'],
                              json_response['terms'])

        # extract entities from text
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/'
            '{}/entities/country/lang/en/extract/'
            .format(inspect.stack()[0][3]),
            method='POST',
            body='{"text": "I want to buy flight tickets for Japan"}')
        self.assertEqual(response.code, 200)
        self.assertItemsEqual(['Japan'], json.loads(response.body)['result'])

    def test_extract_with_grammar(self):
        """
        Test extract terms with specific grammar
        """
        response = self.fetch(
            '/database/0/prefix/extract_api_test/registries/{}/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # add entity
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/{}/entities/tourism/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)
        # add entity language
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/tourism/lang/en/'
            .format(inspect.stack()[0][3]),
            method='POST', body='')
        self.assertEqual(response.code, 200)

        # add terms
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/tourism/lang/en/terms/'
            .format(inspect.stack()[0][3]),
            method='POST',
            body=json.dumps({'terms': ['flight tickets']}))
        self.assertEqual(response.code, 200)

        # extract entities from text
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/tourism/lang/en/extract/'
            .format(inspect.stack()[0][3]),
            method='POST',
            body=json.dumps({
                'text': 'I want to buy flight tickets for Japan',
                'grammar': 'NE : {<NNP|NNPS>*<DT>?<NNP>+}'
            }))
        self.assertEqual(response.code, 200)
        self.assertNotIn('flight tickets', json.loads(response.body)['result'])

        # extract entities from text
        response = self.fetch(
            '/database/0/prefix/terms_api_test/registries/' +
            '{}/entities/tourism/lang/en/extract/'
            .format(inspect.stack()[0][3]),
            method='POST',
            body=json.dumps({
                'text': 'I want to buy flight tickets for Japan',
                'grammar': 'NE : {<NN>*<DT>?<NNS>+}'
            }))
        self.assertEqual(response.code, 200)
        self.assertIn('flight tickets', json.loads(response.body)['result'])


if __name__ == '__main__':
    unittest.main()

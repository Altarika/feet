# -*- coding: utf8 -*-
# test_entities.py
# Test the feet.entities.nlp module
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from feet.entities.nlp import Parser
import unittest


class NLPEntitiesTests(unittest.TestCase):
    def setup(self):
        pass

    def test_extract_entities(self):
        """
        Test
        """
        text = 'The United Nations (UN) is an intergovernmental organization '\
            'to promote international co-operation. A replacement for the '\
            'ineffective League of Nations, the organization was established '\
            'on 24 October 1945 after World War II in order to prevent '\
            'another such conflict. At its founding, the UN had 51 member '\
            'states; there are now 193. The headquarters of the United '\
            'Nations is in Manhattan, New York City, and experiences '\
            'extraterritoriality. Further main offices are situated in '\
            'Geneva, Nairobi, and Vienna. The organization is financed by '\
            'assessed and voluntary contributions from its member states. '\
            'Its objectives include maintaining international peace and '\
            'security, promoting human rights, fostering social and economic '\
            'development, protecting the environment, and providing '\
            'humanitarian aid in cases of famine, natural disaster, and armed '\
            'conflict.'
        # probleme with World War II not concatenated
        # we may take also NN and NNS with combination of CC and IN
        grammar = 'NE : {<NNP|NNPS|NN>*?<NNP|NNPS|JJ|NNS|NN>+}'
        result = Parser().extract_entities(text, grammar)
        self.assertEqual(result[0][1], 'english')
        self.assertTrue('intergovernmental organization' in result[0][0])


if __name__ == '__main__':
    unittest.main()

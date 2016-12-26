# tests
# Testing for the feet module
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
Testing for the feet module
"""

import unittest

TEST_VERSION = "0.1.0"


class InitializationTest(unittest.TestCase):
    def test_import(self):
        """
        Can import feet
        """
        try:
            import feet
        except ImportError:
            self.fail("Unable to import the feet module!")

    def test_version(self):
        """
        Assert that the version is sane
        """
        import feet.version
        self.assertEqual(TEST_VERSION, feet.version.__version__)


if __name__ == '__main__':
    unittest.main()

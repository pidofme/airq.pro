#!/usr/bin/env python
# -*- coding: utf-8 -*-

import airq
import unittest


class AirqTestCase(unittest.TestCase):
    """Airq tests"""

    def setUp(self):
        airq.app.debug = False
        self.app = airq.app.test_client()

    def test_empty_location(self):
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

    def test_location(self):
        res = self.app.get('/beijing')
        self.assertEqual(res.status_code, 200)

    def test_unicode_location(self):
        res = self.app.get('/北京')
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()

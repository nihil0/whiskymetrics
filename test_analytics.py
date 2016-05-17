#!/usr/bin/env python
# coding: utf-8

import analytics, unittest

class TestAnalytics(unittest.TestCase):
    def test_clean(self):
        with open('static/sample_text.txt') as f:
            sample = f.read()

        with open('static/clean_sample.txt') as f:
            clean_sample = f.read()

        self.assertEqual(analytics.clean(sample),clean_sample)

    def test_tokenize(self):
        text = "He's not the Messiah. He's a very naughty boy! Now, piss off!"
        self.assertListEqual(analytics.tokenize(analytics.clean(text)),
                ['hes', 'messiah', 'hes', 'naughty', 'boy', 'piss'])

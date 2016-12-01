#!/usr/bin/env python
# coding: utf-8

import scrub, unittest
import numpy as np

class TestScrub(unittest.TestCase):
    def test_clean(self):
        with open('static/sample_text.txt') as f:
            sample = f.read()

        with open('static/clean_sample.txt') as f:
            clean_sample = f.read()

        self.assertEqual(scrub.clean(sample),clean_sample)

    def test_tokenize(self):
        text = "He's not the Messiah. He's a very naughty boy! Now, piss off!"
        self.assertListEqual(scrub.tokenize(scrub.clean(text)),
                ['hes', 'messiah', 'hes', 'naughty', 'boy', 'piss'])

    def test_represent(self):
        text = ['foo','bar','name','baz','nose color', 'colour','moo',
                'heh','finish','tasty','taste finish']
        (segments,V) = scrub.represent(text,'name')

        s = np.array([ 0.,  0.,  1.,  0.,  2.,  1.,  0.,  0.,  1.,  0.,  2.])
        self.assertTrue(np.array_equal(V.sum(1),s))

        text.pop(2)

        (segments,V) = scrub.represent(text,'name')
        s = np.array([ 1.,  0., 0.,  0.,  2.,  1.,  0.,  0.,  1.,  0.,  2.])
        self.assertTrue(np.array_equal(V.sum(1),s))

    def test_relevant_segment_index(self):
        V = np.array([[1,0,0,0,0],[0,0,0,0,0]])

        self.assertFalse(scrub.relevant_segment_index(V))

        V = np.array([[ 0.,  0.,  0.,  0.,  0.],
        [ 0.,  0.,  0.,  0.,  0.],
        [ 0.,  0.,  1.,  0.,  0.],
        [ 0.,  0.,  0.,  1.,  0.],
        [ 0.,  0.,  0.,  0.,  1.],
        [ 0.,  0.,  0.,  0.,  0.],
        [ 0.,  0.,  0.,  0.,  0.],
        [ 1.,  0.,  0.,  0.,  0.],
        [ 0.,  0.,  1.,  0.,  0.],
        [ 0.,  0.,  0.,  1.,  0.],
        [ 0.,  0.,  0.,  0.,  1.],
        [ 0.,  0.,  0.,  0.,  0.]])

        self.assertListEqual(scrub.relevant_segment_index(V),[7,8,9,10])


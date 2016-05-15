import unittest
from scrape import WhiskyDB


class TestWhiskyDB(unittest.TestCase):
    def setUp(self):
        self.whiskydb = WhiskyDB('static/whisky.db')

    def test_whisky_name(self):
        test_name = 'Talisker 10'
        urls = self.whiskydb.get_post_links(name=test_name)
        num_url = sum((1 for m in urls))
        self.assertEqual(num_url,119)

    def test_whisky_region(self):
        test_region = 'Highland'
        urls = self.whiskydb.get_post_links(region=test_region)
        num_url = sum((1 for m in urls))
        self.assertEqual(num_url,635)

    def test_whisky_distillery(self):
        test_distillery = 'Highland Park'
        urls = self.whiskydb.get_post_links(distillery=test_distillery)
        num_url = sum((1 for m in urls))
        self.assertEqual(num_url,380)




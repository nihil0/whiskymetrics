import unittest
from scrape import WhiskyDB


class TestWhiskyDB(unittest.TestCase):
    def setUp(self):
        self.whiskydb = WhiskyDB()

    def test_whisky_name(self):
        test_name = 'laphroaig 10'
        urls = self.whiskydb.get_post_links(name=test_name)
        num_url = sum((1 for m in urls))
        self.assertEqual(num_url,129)

    def test_whisky_region(self):
        test_region = 'islay'
        urls = self.whiskydb.get_post_links(region=test_region)
        num_url = sum((1 for m in urls))
        self.assertEqual(num_url,731)

    def test_whisky_distillery(self):
        test_distillery = 'laphroaig'
        urls = self.whiskydb.get_post_links(distillery=test_distillery)
        num_url = sum((1 for m in urls))
        self.assertEqual(num_url,731)




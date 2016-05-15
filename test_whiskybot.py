import unittest,scrape

class TestWhiskyBot(unittest.TestCase):
    def setUp(self):
        self.bot = scrape.WhiskyBot()

    def test_legit_post(self):
        text=self.bot.get_review_text('3rywqp')
        with open('static/sample_text.txt','r') as f:
            sample_text = f.read()

        self.assertEqual(text,sample_text)

        text = self.bot.get_review_text(url='https://www.reddit.com/r/bourbon/comments/3rywqp/review_59_1792_port_finish/')
        self.assertEqual(text,sample_text)

    def test_bad_post(self):
        self.assertRaises(Exception,self.bot.get_review_text,'23rywqp')

    def tearDown(self):
        del(self.bot)

import unittest
from spider import crawler


class MyTestCase(unittest.TestCase):
    def says_hello(self):
        crawler = crawler.Crawler()
        self.assertEqual(crawler.say_hi(), "Hello!")


if __name__ == "__main__":
    unittest.main()

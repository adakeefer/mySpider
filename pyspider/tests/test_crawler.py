import sys
import three_spiders.crawler as crawler


def update_path():
    sys.path.append("src/three_spiders")


def test_crawler_says_hello():
    update_path()
    test_crawler = crawler.Crawler()
    assert test_crawler.say_hi() is None

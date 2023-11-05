import crawler


def test_crawler_says_hello():
    test_crawler = crawler.Crawler()
    assert test_crawler.say_hi() is None

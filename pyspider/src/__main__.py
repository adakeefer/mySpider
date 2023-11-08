from crawler import Crawler

if __name__ == "__main__":
    # inspect sys.argv here
    crawler = Crawler()
    crawler.receive_frontier_message()
    crawler.receive_prioritizer_message()

from prioritizer import Prioritizer
from queue_manager import QueueManager

TEST_URLS = ["wikipedia.com", "apple.com", "google.com"]

if __name__ == "__main__":
    # inspect sys.argv here
    qManager = QueueManager()
    prioritizer = Prioritizer()
    for url in TEST_URLS:
        print("Sending msg:", url)
        print(prioritizer._fetch_page_rank(url))
        # qManager.send_to_frontier(url)

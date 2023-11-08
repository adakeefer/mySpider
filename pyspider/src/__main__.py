from prioritizer import Prioritizer
from queue_manager import QueueManager

TEST_URLS = ["https://wikipedia.com", "https://apple.com", "https://google.com"]

if __name__ == "__main__":
    # inspect sys.argv here
    qManager = QueueManager()
    for url in TEST_URLS:
        print("Sending msg: {}", url)
        qManager.send_to_frontier(url)

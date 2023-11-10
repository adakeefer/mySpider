from prioritizer import Prioritizer
from queue_manager import QueueManager

TEST_URLS = ["wikipedia.com", "apple.com", "google.com", "domcop.com"]

if __name__ == "__main__":
    # inspect sys.argv here
    qManager = QueueManager()
    prioritizer = Prioritizer()
    print("Sending msg:", TEST_URLS)
    out = prioritizer._fetch_page_rank(TEST_URLS)
    print(out)
    for entry in out:
        print(
            f"chose {prioritizer._choose_queue_for_page_rank(entry)} for {entry['domain']}"
        )
    # qManager.send_to_frontier(url)

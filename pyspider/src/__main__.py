from prioritizer import Prioritizer
from politeness_router import PolitenessRouter
from queue_manager import QueueManager
import time

TEST_URLS = ["wikipedia.com", "apple.com", "google.com", "domcop.com"]


def random_priority(ptizer: Prioritizer):
    out = ptizer._fetch_page_rank(TEST_URLS)
    print(out)
    for entry in out:
        print(
            f"chose {ptizer._choose_queue_for_page_rank(entry)} for {entry['domain']}"
        )


def prioritize_with_queues(
    q_manager: QueueManager, ptizer: Prioritizer, router: PolitenessRouter
):
    for url in TEST_URLS:
        q_manager.send_to_frontier(url)
    time.sleep(3)
    ptizer.consume()
    router.consume()
    router.consume()
    ptizer.consume()
    router.consume()
    router.consume()


if __name__ == "__main__":
    # inspect sys.argv here
    qManager = QueueManager()
    prioritizer = Prioritizer()
    politeness_router = PolitenessRouter()
    print("Sending msg:", TEST_URLS)
    prioritize_with_queues(qManager, prioritizer, politeness_router)

from prioritizer import Prioritizer
from politeness_router import PolitenessRouter
from queue_manager import QueueManager
from cache_manager import CacheManager
import time

TEST_URLS = [
    "http://www.wikipedia.com",
    "http://www.apple.com",
    "http://www.google.com/maps",
    "http://www.domcop.com/openpagerank/documentation",
]


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


def check_cache():
    cache = CacheManager()
    cache.put("google.com", 1)
    print(f'pulling from cache: {cache.get("google.com")}')
    print(f'not in cache: {cache.get("garbage")}')


if __name__ == "__main__":
    # inspect sys.argv here
    qManager = QueueManager()
    prioritizer = Prioritizer()
    politeness_router = PolitenessRouter()
    print("Sending msg:", TEST_URLS)
    prioritize_with_queues(qManager, prioritizer, politeness_router)

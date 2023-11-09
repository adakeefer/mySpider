import queue_manager
import requests
from config import prioritizer_queue_configs as pqconfigs
from config import page_rank_api_url
from config import page_rank_request_headers


class Prioritizer:
    def __init__(self):
        self.queue_manager = queue_manager.QueueManager()
        self.queue_keys = [x.queue_id for x in pqconfigs]
        self.queue_weights = [x.weight for x in pqconfigs]

    def consume(self):
        msgs = self.queue_manager.receive_from_frontier(num_messages=3)
        msg_ids = []
        receipt_ids = []
        for msg in msgs:
            url = msg.body
            print("Prioritizer received url:", url)
            target_queue_id = self.prioritize(url)
            if target_queue_id > 0:
                self.publish(target_queue_id, url)
            msg_ids.append(msg.message_id)
            receipt_ids.append(msg.receipt_handle)

        self.queue_manager.delete_from_frontier(msg_ids, receipt_ids)
        print("Prioritizer removed messages")

    def prioritize(self, url):
        page_rank = 0
        try:
            page_rank = self._fetch_page_rank(url)
        except Exception as e:
            print("Error fetching pagerank for url {}. Skipping. Error={}", url, e)

        # TODO: map this to priority
        return page_rank

    def publish(self, target_queue_id, url):
        print("Publishing url {} to queue {}", url, target_queue_id)
        self.queue_manager.send_to_prioritizer_n(target_queue_id, url)

    def _fetch_page_rank(self, url):
        params = {"domains[]": ",".join([url])}
        response = requests.get(
            page_rank_api_url, headers=page_rank_request_headers, params=params
        )
        response.raise_for_status()
        ranks = response.json()["response"]
        return ranks
        # return ranks[0]["page_rank_integer"]

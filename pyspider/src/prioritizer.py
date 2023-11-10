import queue_manager
import requests
import config
import random


class Prioritizer:
    def __init__(self):
        self.queue_manager = queue_manager.QueueManager()
        self.queue_keys = [x.queue_id for x in config.prioritizer_queue_configs]
        self.queue_weights = [x.weight for x in config.prioritizer_queue_configs]

    def consume(self):
        msgs = self.queue_manager.receive_from_frontier(num_messages=3)
        msg_ids = []
        receipt_ids = []
        domains = []
        for msg in msgs:
            domains.append(msg.body)
            print("Prioritizer received url:", msg.body)
            msg_ids.append(msg.message_id)
            receipt_ids.append(msg.receipt_handle)

        url_to_target_queue_id = self.prioritize(domains)
        for url, target_queue_id in url_to_target_queue_id.items():
            if target_queue_id > 0:
                self.publish(target_queue_id, url)

        self.queue_manager.delete_from_frontier(msg_ids, receipt_ids)
        print("Prioritizer removed messages")

    def prioritize(self, domains):
        try:
            page_rank = self._fetch_page_rank(domains)
        except Exception as e:
            print(f"Error fetching pagerank for domains {domains}. Skipping. Error={e}")
            return 0

        print(f"page_rank: {page_rank}")
        return dict(zip(domains, map(self._choose_queue_for_page_rank, page_rank)))

    def publish(self, target_queue_id, url):
        print(f"Publishing url {url} to queue {target_queue_id}")
        self.queue_manager.send_to_prioritizer_n(target_queue_id, url)

    def _fetch_page_rank(self, domain_list):
        params = {"domains[]": domain_list}
        response = requests.get(
            config.page_rank_api_url,
            headers=config.page_rank_request_headers,
            params=params,
        )
        response.raise_for_status()
        ranks = response.json()["response"]
        return ranks

    # Use linear interpolation to bias weights based on input page rank
    # higher page rank, more likely we are to choose heavily weighted queues
    # lower page rank, more likely we are to choose lower weight queues
    def _choose_queue_for_page_rank(self, page_rank_entry):
        rank = page_rank_entry["page_rank_decimal"]
        if rank < 0.0:
            print(f"Warning: rank < 0 found: {rank}. Normalizing to 0")
            rank = 0.0
        elif rank > 10.01:
            print(f"Warning: rank > max found: {rank}. Normalizing to max")
            rank = 9.99999

        normalized_rank = rank / 10.0
        bias = normalized_rank
        updated_queue_weights = [
            w * bias + (100 - w) * (1 - bias) for w in self.queue_weights
        ]
        print(
            f"Normalized rank: {normalized_rank}, Updated queue weights:{updated_queue_weights}"
        )
        return random.choices(self.queue_keys, updated_queue_weights)[0]

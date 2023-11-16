import queue_manager
import cache_manager
import random
import config
from urllib.parse import urlparse


class PolitenessRouter:
    def __init__(self):
        self.queue_manager = queue_manager.QueueManager()
        self.cache_manager = cache_manager.CacheManager()
        self.prioritizer_queue_keys = [
            x.queue_config.queue_id for x in config.prioritizer_queue_configs
        ]
        self.prioritizer_queue_weights = [
            x.weight for x in config.prioritizer_queue_configs
        ]
        self.worker_ids = [x.queue_id for x in config.worker_queue_configs]
        self.worker_weights = [
            100 // len(config.worker_queue_configs) for _ in config.worker_queue_configs
        ]

    def consume(self):
        queue_id = self._choose_random_prioritizer_queue()
        msgs = self.queue_manager.receive_from_prioritizer_n(queue_id, num_messages=5)
        if len(msgs) == 0:
            pass
        msg_ids = []
        receipt_ids = []
        for msg in msgs:
            url = msg.body
            print(f"PolitenessRouter received url: {url}")
            msg_ids.append(msg.message_id)
            receipt_ids.append(msg.receipt_handle)
            worker_id = self.select_worker(url)
            self.publish(worker_id, url)

        self.queue_manager.delete_from_prioritizer_n(queue_id, msg_ids, receipt_ids)

    def select_worker(self, url):
        res = urlparse(url)
        domain = res.netloc
        worker_id = self.cache_manager.get(domain)
        if worker_id is None:
            worker_id = self._choose_random_worker()
            print(f"cache miss on domain {domain} choosing random worker {worker_id}")
            self.cache_manager.put(domain, worker_id)
        worker_id = int(worker_id)
        self._rebalance_weights(worker_id)
        return worker_id

    def publish(self, worker_id, url):
        print(f"Publishing url {url} to worker {worker_id}")
        self.queue_manager.send_to_worker_n(worker_id, url)

    def _choose_random_prioritizer_queue(self):
        return random.choices(
            self.prioritizer_queue_keys, self.prioritizer_queue_weights
        )[0]

    def _rebalance_weights(self, chosen_worker_id):
        if chosen_worker_id <= 0 or chosen_worker_id > len(self.worker_weights):
            print(f"invalid worker id chosen for rebalance {chosen_worker_id}")
            return
        for i in range(0, len(self.worker_weights)):
            if i + 1 == chosen_worker_id:
                self.worker_weights[i] //= config.rebalance_factor
            else:
                self.worker_weights[i] *= config.rebalance_factor

    def _choose_random_worker(self):
        return random.choices(self.worker_ids, self.worker_weights)[0]

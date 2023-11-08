import queue_manager
import random
from config import prioritizer_queue_configs as pqconfigs


class PolitenessRouter:
    def __init__(self):
        self.queue_manager = queue_manager.QueueManager()
        self.prioritizer_queue_keys = [x.queue_id for x in pqconfigs]
        self.prioritizer_queue_weights = [x.weight for x in pqconfigs]

    def consume(self):
        queue_id = self._choose_weighted_queue()
        msgs = self.queue_manager.receive_from_prioritizer_n(queue_id, num_messages=3)
        msg_ids = []
        receipt_ids = []
        for msg in msgs:
            url = msg.body
            print("PolitenessRouter received url: {}", url)
            msg_ids.append(msg.message_id)
            receipt_ids.append(msg.receipt_handle)
        self.queue_manager.delete_from_prioritizer_n(queue_id, msg_ids, receipt_ids)
        print("PolitenessRouter removed messages")

    def _choose_weighted_queue(self):
        return random.choices(
            self.prioritizer_queue_keys, self.prioritizer_queue_weights
        )[0]

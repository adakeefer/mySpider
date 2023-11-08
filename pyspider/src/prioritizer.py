import queue_manager
import random
from config import prioritizer_queue_config as pqconfig


class Prioritizer:
    def __init__(self):
        self.queue_manager = queue_manager.QueueManager()
        self.queue_keys = [x["id"] for x in pqconfig]
        self.queue_weights = [x["weight"] for x in pqconfig]

    def consume(self):
        msgs = self.queue_manager.receive_from_frontier()
        for msg in msgs:
            target_queue_id = self.prioritize(msg.body)
            self.publish(target_queue_id, msg.body)

    def prioritize(self, url):
        return 1

    def publish(self, target_queue_id, url):
        self.queue_manager.send_to_prioritizer_n(target_queue_id, url)

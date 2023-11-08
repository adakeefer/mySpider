import boto3
from botocore.config import Config
from config import prioritizer_queue_config as pqconfig


class QueueManager:
    def __init__(self):
        self.sqs = boto3.resource("sqs", config=Config(region_name="us-east-2"))
        self.url_frontier = self.sqs.Queue(
            "https://sqs.us-east-2.amazonaws.com/061767223458/URLFrontierQueue"
        )
        self.prioritizer_queues = self._create_prioritizer_queues()

    def _create_prioritizer_queues(self):
        queues_by_id = {}
        for qconfig in pqconfig:
            queues_by_id[qconfig["id"]] = self.sqs.Queue(qconfig["url"])

        return queues_by_id

    def _check_id_in_range(self, id: int):
        if id > len(self.prioritizer_queues) or id <= 0:
            raise ValueError("Id must reference prioritizer queues 1...n")

    def receive_from_prioritizer_n(self, id: int, num_messages=1):
        self._check_id_in_range(id)
        return self.prioritizer_queues[id].receive_messages(
            MaxNumberOfMessages=num_messages
        )

    def send_to_prioritizer_n(self, id: int, message_body: str):
        self._check_id_in_range(id)
        self.prioritizer_queues[id].send_message(MessageBody=message_body)

    def receive_from_frontier(self, num_messages=1):
        return self.url_frontier.receive_messages(MaxNumberOfMessages=num_messages)

    def send_to_frontier(self, message_body):
        self.url_frontier.send_message(MessageBody=message_body)

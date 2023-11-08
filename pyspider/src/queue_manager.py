import boto3
from botocore.config import Config


class QueueManager:
    def __init__(self):
        self.sqs = boto3.resource("sqs", config=Config(region_name="us-east-2"))
        self.url_frontier = self.sqs.Queue(
            "https://sqs.us-east-2.amazonaws.com/061767223458/URLFrontierQueue"
        )
        self.prioritizer_queues = self._create_prioritizer_queues()

    def _create_prioritizer_queues(self):
        queues_by_number = {
            1: self.sqs.Queue(
                "https://sqs.us-east-2.amazonaws.com/061767223458/prioritizerQueue1"
            ),
            2: self.sqs.Queue(
                "https://sqs.us-east-2.amazonaws.com/061767223458/prioritizerQueue2"
            ),
        }
        return queues_by_number

    def _check_priority_in_range(self, priority: int):
        if priority > len(self.prioritizer_queues) or priority <= 0:
            raise ValueError("Priority must reference prioritizer queues 1...n")

    def receive_from_prioritizer_n(self, priority: int, num_messages=1):
        self._check_priority_in_range(priority)
        return self.prioritizer_queues[priority].receive_messages(
            MaxNumberOfMessages=num_messages
        )

    def send_to_prioritizer_n(self, priority: int, message_body: str):
        self._check_priority_in_range(priority)
        self.prioritizer_queues[priority].send_message(MessageBody=message_body)

    def receive_from_frontier(self, num_messages=1):
        return self.url_frontier.receive_messages(MaxNumberOfMessages=num_messages)

    def send_to_frontier(self, message_body):
        self.url_frontier.send_message(MessageBody=message_body)

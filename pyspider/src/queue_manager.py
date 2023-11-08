import boto3
from botocore.config import Config
from config import prioritizer_queue_configs as pqconfigs


class QueueManager:
    def __init__(self):
        self.sqs = boto3.resource("sqs", config=Config(region_name="us-east-2"))
        self.url_frontier = self.sqs.Queue(
            "https://sqs.us-east-2.amazonaws.com/061767223458/URLFrontierQueue"
        )
        self.prioritizer_queues = self._create_prioritizer_queues()

    def receive_from_prioritizer_n(self, queue_id: int, num_messages=1):
        self._check_id_in_range(queue_id)
        return self.prioritizer_queues[queue_id].receive_messages(
            MaxNumberOfMessages=num_messages
        )

    def send_to_prioritizer_n(self, queue_id: int, message_body: str):
        self._check_id_in_range(queue_id)
        self.prioritizer_queues[queue_id].send_message(MessageBody=message_body)

    def delete_from_prioritizer_n(
        self, queue_id: int, msg_ids: list[int], receipt_ids: list[int]
    ):
        self._check_id_in_range(queue_id)
        entries = self._build_delete_request(msg_ids, receipt_ids)
        self.prioritizer_queues[queue_id].delete_messages(entries)

    def receive_from_frontier(self, num_messages=1):
        return self.url_frontier.receive_messages(MaxNumberOfMessages=num_messages)

    def send_to_frontier(self, message_body):
        self.url_frontier.send_message(MessageBody=message_body)

    def delete_from_frontier(self, msg_ids: list[int], receipt_ids: list[int]):
        entries = self._build_delete_request(msg_ids, receipt_ids)
        self.url_frontier.delete_messages(entries)

    def _create_prioritizer_queues(self):
        queues_by_id = {}
        for qconfig in pqconfigs:
            queues_by_id[qconfig.queue_id] = self.sqs.Queue(qconfig.url)

        return queues_by_id

    def _check_id_in_range(self, queue_id: int):
        if queue_id not in self.prioritizer_queues:
            raise ValueError("Id must reference prioritizer queues 1...n")

    def _build_delete_request(self, msg_ids, receipt_ids):
        if len(msg_ids) == 0 or len(receipt_ids) == 0:
            raise ValueError("msg_ids and receipt_ids must be non-empty")
        elif len(msg_ids) != len(receipt_ids):
            raise ValueError(
                "A msg_id and receipt_id must be supplied for each message to delete"
            )
        return [
            {"Id": msg_id, "ReceiptHandle": receipt_id}
            for msg_id, receipt_id in zip(msg_ids, receipt_ids)
        ]

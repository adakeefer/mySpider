import boto3
from botocore.config import Config


class QueueManager:
    def __init__(self):
        sqs = boto3.resource("sqs", config=Config(region_name="us-east-2"))
        self.queue = sqs.Queue(
            "https://sqs.us-east-2.amazonaws.com/061767223458/URLFrontierQueue"
        )

    def receive(self):
        msgs = self.queue.receive_messages()
        print(msgs[0].body)

    def send(self):
        self.queue.send_message(MessageBody="hello adam!!!")

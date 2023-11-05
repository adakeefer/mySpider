import pika


class QueueManager:
    def __init__(self):
        self.connection = self.open_connection()
        self.channel = self.connection.channel()
        self.create_queues()

    def __del__(self):
        self.connection.close()

    def open_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters("localhost"))

    def create_queues(self):
        self.channel.queue_declare(queue="hello")

    def say_hi(self):
        self.channel.basic_publish(
            exchange="", routing_key="hello", body="Hello World!"
        )
        print(" [x] Sent 'Hello World!'")

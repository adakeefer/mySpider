from queue_manager import QueueManager


class Crawler:
    def __init__(self):
        self.queue_manager = QueueManager()

    def receive_frontier_message(self):
        self.queue_manager.send_to_frontier("https://apple.com")
        msgs = self.queue_manager.receive_from_frontier()
        print(msgs[0].body)

    def receive_prioritizer_message(self):
        self.queue_manager.send_to_prioritizer_n(1, "https://wikipedia.com")
        msgs = self.queue_manager.receive_from_prioritizer_n(1)
        print(msgs[0].body)

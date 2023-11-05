from queue_manager import QueueManager


class Crawler:
    def __init__(self):
        self.value1 = 1

    def say_hi(self):
        print("Hello!")

    def connect(self):
        queue_manager = QueueManager()
        queue_manager.say_hi()

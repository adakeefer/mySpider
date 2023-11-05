class Prioritizer:
    def __init__(self):
        self.queuesByPriority = {}

    def consume(self, url):
        priority = self.prioritize(url)
        queue = self.queuesByPriority[priority]
        self.publish(queue, url)

    def prioritize(self, url):
        return 1

    def publish(self, url):
        return None

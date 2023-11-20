class QueueConfig:
    def __init__(self, queue_id, url):
        self.queue_id = queue_id
        self.url = url


class PrioritizerQueueConfig:
    def __init__(self, queue_id, url, weight):
        self.queue_config = QueueConfig(queue_id, url)
        self.weight = weight


prioritizer_queue_configs = [
    PrioritizerQueueConfig(
        1, "https://sqs.us-east-2.amazonaws.com/YOUR_URL_HERE", 80
    ),
    PrioritizerQueueConfig(
        2, "https://sqs.us-east-2.amazonaws.com/YOUR_URL_HERE", 20
    ),
]
worker_queue_configs = [
    QueueConfig(1, "https://sqs.us-east-2.amazonaws.com/YOUR_URL_HERE"),
    QueueConfig(2, "https://sqs.us-east-2.amazonaws.com/YOUR_URL_HERE"),
]
aws_region = "YOUR_REGION_HERE"
url_frontier_url = "https://sqs.us-east-2.amazonaws.com/YOUR_URL_HERE"
page_rank_api_url = "https://openpagerank.com/api/v1.0/getPageRank"
page_rank_api_key = "YOUR_API_KEY_HERE"
page_rank_request_headers = {"API-OPR": page_rank_api_key}
redis_port = 6379
redis_host = "localhost"
redis_default_expiry_seconds = 60
rebalance_factor = 2

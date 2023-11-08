class PrioritizerQueueConfig:
    def __init__(self, queue_id, url, weight):
        self.queue_id = queue_id
        self.url = url
        self.weight = weight


prioritizer_queue_configs = [
    PrioritizerQueueConfig(
        1, "https://sqs.us-east-2.amazonaws.com/061767223458/prioritizerQueue1", 70
    ),
    PrioritizerQueueConfig(
        2, "https://sqs.us-east-2.amazonaws.com/061767223458/prioritizerQueue2", 30
    ),
]
page_rank_api_url = "https://openpagerank.com/api/v1.0/getPageRank"
page_rank_api_key = "8o4scsssoc44gokcwkk0cw8gg8g0kcwoowwscoso"
page_rank_request_headers = {"API-OPR": page_rank_api_key}

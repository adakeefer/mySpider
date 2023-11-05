from prioritizer.prioritizer import Prioritizer


def test_prioritizer_prioritize_returns_priority():
    prioritizer = Prioritizer()
    assert prioritizer.prioritize("name") == 1

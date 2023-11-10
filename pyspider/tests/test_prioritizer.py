import pytest
from unittest.mock import Mock
import queue_manager
from prioritizer import Prioritizer


@pytest.fixture
def mock_qmanager(mocker):
    mock = Mock(spec=queue_manager.QueueManager())
    mocker.patch("queue_manager.QueueManager", return_value=mock)
    mock_msg = Mock()
    mock_msg.body = "test.com"
    mock_msg.message_id = "1"
    mock_msg.receipt_handle = "2"
    mock_msg2 = Mock()
    mock_msg2.body = "name.com"
    mock_msg2.message_id = "3"
    mock_msg2.receipt_handle = "4"
    mock.receive_from_frontier.return_value = [mock_msg, mock_msg2]
    return mock


def mock_page_rank_call(mocker, domains):
    mock_response = Mock()

    def compute_response():
        return {
            "response": [
                {
                    "status_code": 200,
                    "error": "",
                    "page_rank_integer": 1,
                    "page_rank_decimal": 1,
                    "rank": "1",
                    "domain": x,
                }
                for x in domains
            ]
        }

    mock_response.json.return_value = compute_response()
    mocker.patch("requests.get", return_value=mock_response)


@pytest.fixture
def mock_random(mocker):
    mocker.patch("random.choices", return_value=[1])


@pytest.fixture
def create_ptizer(mock_qmanager):
    return Prioritizer()


def test_fetch_page_rank(create_ptizer, mocker):
    expected_response = [
        {
            "status_code": 200,
            "error": "",
            "page_rank_integer": 1,
            "page_rank_decimal": 1,
            "rank": "1",
            "domain": "test.com",
        }
    ]
    mock_page_rank_call(mocker, ["test.com"])
    assert create_ptizer._fetch_page_rank(["test.com"]) == expected_response


def test_prioritize_returns_priority(create_ptizer, mocker, mock_random):
    domains = ["test.com"]
    mock_page_rank_call(mocker, domains)
    assert create_ptizer.prioritize(domains) == {"test.com": 1}
    domains.append("name.com")
    mock_page_rank_call(mocker, domains)
    res = create_ptizer.prioritize(domains)
    assert res["name.com"] is 1
    assert res["test.com"] is 1


def test_publish(create_ptizer):
    assert create_ptizer.publish(1, "test") is None


def test_consume(mock_qmanager, mocker, mock_random):
    mock_page_rank_call(mocker, ["test.com", "name.com"])
    ptizer = Prioritizer()
    ptizer.consume()
    mock_qmanager.receive_from_frontier.assert_called_with(num_messages=5)
    mock_qmanager.send_to_prioritizer_n.assert_any_call(1, "test.com")
    mock_qmanager.send_to_prioritizer_n.assert_any_call(1, "name.com")
    mock_qmanager.delete_from_frontier.assert_called_with(["1", "3"], ["2", "4"])

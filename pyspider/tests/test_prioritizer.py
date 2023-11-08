import pytest
from unittest.mock import Mock
import queue_manager
from prioritizer import Prioritizer


@pytest.fixture
def mock_qmanager(mocker):
    mock = Mock(spec=queue_manager.QueueManager())
    mocker.patch("queue_manager.QueueManager", return_value=mock)
    mock_msg = Mock()
    mock_msg.body = "test"
    mock_msg.message_id = "1"
    mock_msg.receipt_handle = "2"
    mock.receive_from_frontier.return_value = [mock_msg]
    return mock


@pytest.fixture
def mock_page_rank_call(mocker):
    mock_response = Mock()
    mock_response.json.return_value = {
        "response": [
            {
                "status_code": 200,
                "error": "",
                "page_rank_integer": 1,
                "page_rank_decimal": 1,
                "rank": "1",
                "domain": "google.com",
            }
        ]
    }
    mocker.patch("requests.get", return_value=mock_response)


@pytest.fixture
def create_ptizer(mock_qmanager):
    return Prioritizer()


def test_fetch_page_rank(create_ptizer, mock_page_rank_call):
    assert create_ptizer._fetch_page_rank("test") == 1


def test_prioritize_returns_priority(create_ptizer, mock_page_rank_call):
    assert create_ptizer.prioritize("name") == 1


def test_publish(create_ptizer):
    assert create_ptizer.publish(1, "test") is None


def test_consume(mock_qmanager, mock_page_rank_call):
    ptizer = Prioritizer()
    ptizer.consume()
    mock_qmanager.receive_from_frontier.assert_called_with(num_messages=3)
    mock_qmanager.send_to_prioritizer_n.assert_called_with(1, "test")
    mock_qmanager.delete_from_frontier.assert_called_with(["1"], ["2"])

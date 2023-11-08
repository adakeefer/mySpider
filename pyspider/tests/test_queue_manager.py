import boto3
from botocore.config import Config
import pytest
from unittest.mock import Mock
from queue_manager import QueueManager


@pytest.fixture
def mock_sqs(mocker):
    mock = Mock(spec=boto3.resource("sqs", config=Config(region_name="us-east-2")))
    mocker.patch("boto3.resource", return_value=mock)
    return mock


@pytest.fixture
def qmanager(mock_sqs):
    mock_queue = Mock()
    mock_message = Mock()
    mock_message.body = "test"
    mock_queue.receive_messages.return_value = [mock_message]
    mock_sqs.Queue.return_value = mock_queue
    return QueueManager()


def test_queue_manager_creates_queues(mock_sqs):
    mock_queue = Mock()
    mock_sqs.Queue.return_value = mock_queue
    qmanager = QueueManager()
    assert qmanager.sqs is mock_sqs
    assert qmanager.url_frontier is mock_queue
    assert len(qmanager.prioritizer_queues) is 2


def test__check_priority_in_range(qmanager):
    assert qmanager._check_id_in_range(1) is None
    assert qmanager._check_id_in_range(2) is None
    with pytest.raises(ValueError):
        qmanager._check_id_in_range(0)
    with pytest.raises(ValueError):
        qmanager._check_id_in_range(3)


def test_send_receive_url_frontier(qmanager):
    assert qmanager.send_to_frontier("test") is None
    msgs = qmanager.receive_from_frontier()
    assert len(msgs) is 1
    assert msgs[0].body == "test"


def test_send_receive_prioritizer_n(qmanager):
    assert qmanager.send_to_prioritizer_n(1, "test") is None
    msgs = qmanager.receive_from_prioritizer_n(1)
    assert len(msgs) is 1
    assert msgs[0].body == "test"


def test__build_delete_request(qmanager):
    with pytest.raises(ValueError):
        qmanager._build_delete_request([], [])
    with pytest.raises(ValueError):
        qmanager._build_delete_request(["1"], [])
    with pytest.raises(ValueError):
        qmanager._build_delete_request(["1"], ["1", "2"])
    entries = qmanager._build_delete_request(["1", "2"], ["3", "4"])
    assert entries[0] == {"Id": "1", "ReceiptHandle": "3"}
    assert entries[1] == {"Id": "2", "ReceiptHandle": "4"}


def test_delete_from_frontier(qmanager):
    qmanager.delete_from_frontier(["1"], ["3"])
    qmanager.url_frontier.delete_messages.assert_called_with(
        [{"Id": "1", "ReceiptHandle": "3"}]
    )


def test_delete_from_prioritizer_n(qmanager):
    qmanager.delete_from_prioritizer_n(1, ["1"], ["3"])
    qmanager.prioritizer_queues[1].delete_messages.assert_called_with(
        [{"Id": "1", "ReceiptHandle": "3"}]
    )

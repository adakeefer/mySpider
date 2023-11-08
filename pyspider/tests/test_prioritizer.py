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
    mock.receive_from_frontier.return_value = [mock_msg]
    return mock


@pytest.fixture
def create_ptizer(mock_qmanager):
    return Prioritizer()


def test_prioritize_returns_priority(create_ptizer):
    assert create_ptizer.prioritize("name") == 1


def test_publish(create_ptizer):
    assert create_ptizer.publish(1, "test") is None


def test_consume(mock_qmanager):
    ptizer = Prioritizer()
    ptizer.consume()
    mock_qmanager.receive_from_frontier.assert_called()
    mock_qmanager.send_to_prioritizer_n.assert_called_with(1, "test")

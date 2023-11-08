import pytest
from unittest.mock import Mock
import queue_manager
from politeness_router import PolitenessRouter


@pytest.fixture
def mock_qmanager(mocker):
    mock = Mock(spec=queue_manager.QueueManager())
    mocker.patch("queue_manager.QueueManager", return_value=mock)
    mock_msg = Mock()
    mock_msg.body = "test"
    mock_msg.message_id = "1"
    mock_msg.receipt_handle = "2"
    mock.receive_from_prioritizer_n.return_value = [mock_msg]
    return mock


def test_consume(mocker, mock_qmanager):
    politeness_router = PolitenessRouter()
    mocker.patch("random.choices", return_value=[1])
    politeness_router.consume()
    mock_qmanager.receive_from_prioritizer_n.assert_called_with(1, num_messages=3)
    mock_qmanager.delete_from_prioritizer_n.assert_called_with(1, ["1"], ["2"])

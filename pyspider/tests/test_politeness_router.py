import pytest
from unittest.mock import Mock
import queue_manager
import cache_manager
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


@pytest.fixture
def mock_cache_manager(mocker):
    mock = Mock(spec=cache_manager.CacheManager())
    mocker.patch("cache_manager.CacheManager", return_value=mock)
    mock.get.return_value = 1
    return mock


@pytest.fixture
def mock_empty_cache_manager(mocker):
    mock = Mock(spec=cache_manager.CacheManager())
    mocker.patch("cache_manager.CacheManager", return_value=mock)
    mock.get.return_value = None
    return mock


@pytest.fixture
def mock_parse_result(mocker):
    mock = Mock()
    mock.netloc = "test"
    mocker.patch("urllib.parse.urlparse", return_value=mock)


def test_consume(mocker, mock_qmanager, mock_cache_manager, mock_parse_result):
    mocker.patch("random.choices", return_value=[1])
    p_router = PolitenessRouter()
    p_router.consume()
    mock_qmanager.receive_from_prioritizer_n.assert_called_with(1, num_messages=5)
    mock_qmanager.delete_from_prioritizer_n.assert_called_with(1, ["1"], ["2"])
    mock_qmanager.send_to_worker_n.assert_called_with(1, "test")


def test_select_worker(mocker, mock_cache_manager, mock_parse_result):
    mocker.patch("random.choices", return_value=[1])
    p_router = PolitenessRouter()
    worker_id = p_router.select_worker("test")
    assert worker_id is 1
    mock_cache_manager.get.assert_called_with("")


def test_select_worker_missing(mocker, mock_empty_cache_manager, mock_parse_result):
    mocker.patch("random.choices", return_value=[1])
    p_router = PolitenessRouter()
    worker_id = p_router.select_worker("test")
    assert worker_id is 1
    mock_empty_cache_manager.get.assert_called_with("")
    mock_empty_cache_manager.put.assert_called_with("", 1)


def test_rebalance_weights():
    p_router = PolitenessRouter()
    assert p_router.worker_weights == [50, 50]
    p_router._rebalance_weights(1)
    assert p_router.worker_weights == [25, 100]
    p_router._rebalance_weights(1)
    assert p_router.worker_weights == [12, 200]
    p_router._rebalance_weights(0)
    assert p_router.worker_weights == [12, 200]
    p_router._rebalance_weights(2)
    assert p_router.worker_weights == [24, 100]
    p_router._rebalance_weights(2)
    assert p_router.worker_weights == [48, 50]

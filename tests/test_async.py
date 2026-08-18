"""Tests for asynchronous notification dispatching and event handling."""
import pytest
from app.services.notifications import (
    dispatch_order_alert,
    _send_async_email,
    get_dispatched_count,
    clear_dispatch_log
)


@pytest.mark.asyncio
async def test_clear_dispatch_log():
    """Verify dispatch log can be cleared."""
    clear_dispatch_log()
    assert get_dispatched_count() == 0


@pytest.mark.asyncio
async def test_direct_async_email_success():
    """Verify direct async email function succeeds when awaited."""
    res = await _send_async_email("user@example.com", "Test", "Hello")
    assert res is True
    assert get_dispatched_count() == 1


@pytest.mark.asyncio
async def test_multiple_direct_async_emails():
    """Verify multiple async emails are recorded."""
    clear_dispatch_log()
    await _send_async_email("user1@example.com", "Alert 1", "Msg 1")
    await _send_async_email("user2@example.com", "Alert 2", "Msg 2")
    assert get_dispatched_count() == 2


@pytest.mark.asyncio
async def test_async_order_alert_dispatched_properly():
    """
    BUG 3 Target Test (Incorrect Async Handling):
    Calling dispatch_order_alert must properly await the background dispatch coroutine,
    return True, and record the dispatched alert in the dispatch log.
    Currently fails because dispatch_order_alert fails to await _send_async_email,
    leaving a coroutine unawaited and returning False (or failing the log assertion).
    """
    clear_dispatch_log()
    success = await dispatch_order_alert(
        email="customer@example.com",
        order_id=101,
        total=149.99
    )
    assert success is True, "Expected dispatch_order_alert to return True"
    assert get_dispatched_count() == 1, (
        f"Expected 1 dispatched alert in log, but found {get_dispatched_count()}"
    )

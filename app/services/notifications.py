"""Notification service for dispatching email and webhook alerts asynchronously."""
import asyncio
from typing import Dict, List

# In-memory storage for test verification of dispatched alerts
DISPATCH_LOG: List[Dict[str, str]] = []


async def _send_async_email(email: str, subject: str, message: str) -> bool:
    """Simulate non-blocking async network I/O for sending notification."""
    await asyncio.sleep(0.01)
    DISPATCH_LOG.append({"email": email, "subject": subject, "message": message})
    return True


async def dispatch_order_alert(email: str, order_id: int, total: float) -> bool:
    """
    Dispatch an order confirmation notification.
    
    BUG 3 (Incorrect Async Handling):
    The async function _send_async_email is called WITHOUT 'await'.
    This returns a coroutine object instead of waiting for execution,
    triggering a RuntimeWarning and failing to record the dispatched alert.
    """
    subject = f"Order #{order_id} Confirmed"
    message = f"Your order totaling ${total:.2f} has been processed successfully."
    
    # MISSING AWAIT: Calling coroutine without awaiting it
    result = await _send_async_email(email, subject, message)
    
    return result is True


def get_dispatched_count() -> int:
    """Return number of dispatched messages in the log."""
    return len(DISPATCH_LOG)


def clear_dispatch_log():
    """Clear memory log for test isolation."""
    DISPATCH_LOG.clear()

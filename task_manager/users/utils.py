"""Utilities for working with user objects."""

from typing import Any


def format_user_display(user: Any) -> str:
    """Return a human-friendly representation of a user."""
    full_name = (user.get_full_name() or "").strip()
    return full_name if full_name else user.get_username()

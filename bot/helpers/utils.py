"""
General utility functions for ID Chatbot.
Provides byte formatting and duration readability converters.
"""

from typing import Union


def humanbytes(size: Union[int, float]) -> str:
    """
    Convert a raw byte count into a human-readable string representation (e.g. KB, MB, GB).

    :param size: Number of bytes.
    :return: Formatted string (e.g., '12.45 MB', '1.02 GB').
    """
    if not size or size <= 0:
        return "0 B"

    power = 1024
    unit_index = 0
    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    size_val = float(size)
    while size_val >= power and unit_index < len(units) - 1:
        size_val /= power
        unit_index += 1

    return f"{size_val:.2f} {units[unit_index]}"


def get_readable_time(seconds: Union[int, float]) -> str:
    """
    Convert total seconds into a readable time string in '2h 30m 15s' format.

    :param seconds: Total duration in seconds.
    :return: Human readable time string (e.g., '2h 30m 15s', '45s').
    """
    total_seconds = int(seconds)
    if total_seconds <= 0:
        return "0s"

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)

    time_components = []
    if days > 0:
        time_components.append(f"{days}d")
    if hours > 0:
        time_components.append(f"{hours}h")
    if minutes > 0:
        time_components.append(f"{minutes}m")
    if secs > 0 or not time_components:
        time_components.append(f"{secs}s")

    return " ".join(time_components)

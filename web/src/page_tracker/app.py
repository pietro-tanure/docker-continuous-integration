"""
app.py

Immplement Flask web application for tracking page views stored persistently
in a Redis data store
"""

import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    """
    Handles the request to the index route of the application.

    Returns:
        str: A message indicating the number of times the page has been viewed.
        int: The HTTP status code (200 for success, 500 for Redis error).

    Raises:
        RedisError: If there is an issue with Redis during the page view count
        update.
    """
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")  # pylint: disable=E1101
        return "Sorry, something went wrong \N{pensive face}", 500
    return f"This page has been seen {page_views} times."


@cache
def redis():
    """
    Creates and returns a Redis client instance configured with the URL
    specified in the environment variable `REDIS_URL`. If the environment
    variable is not set, it defaults to a Redis server running on localhost
    at port 6379.

    Returns:
        Redis: An instance of the Redis client connected to the specified URL.

    Example:
        >>> redis_client = redis()
        >>> redis_client.set('key', 'value')
        True
    """
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

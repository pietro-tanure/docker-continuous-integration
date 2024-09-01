import pytest
import requests


@pytest.mark.timeout(1.5)
def test_should_update_redis(redis_client, flask_url):
    # Given
    redis_client.set("page_views", 4)

    # When
    response = requests.get(flask_url)

    # Then
    assert response.status_code == 200
    assert response.text == "This page has been seen 5 times."
    assert redis_client.get("page_views") == b"5"


# docker start redis-server
# flask --app page_tracker.app run
# python -m pytest -v test/e2e/ \
#   --flask-url http://127.0.0.1:5000 \
#   --redis-url redis://127.0.0.1:6379

import copy
import pytest
import server
from server import app


ORIGINAL_CLUBS = copy.deepcopy(server.clubs)
ORIGINAL_COMPETITIONS = copy.deepcopy(server.competitions)


@pytest.fixture()
def client():
    app.config["TESTING"] = True

    server.clubs = copy.deepcopy(ORIGINAL_CLUBS)
    server.competitions = copy.deepcopy(ORIGINAL_COMPETITIONS)

    return app.test_client()
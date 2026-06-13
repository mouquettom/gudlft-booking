import copy
import pytest
import server
from server import app


# On garde une copie propre des données initiales
ORIGINAL_CLUBS = copy.deepcopy(server.clubs)
ORIGINAL_COMPETITIONS = copy.deepcopy(server.competitions)


# Fixture pytest : fonction réutilisable automatiquement dans les tests
@pytest.fixture()
def client():
    app.config["TESTING"] = True

    # Avant chaque test, on remet les clubs et compétitions à leur état initial
    server.clubs = copy.deepcopy(ORIGINAL_CLUBS)
    server.competitions = copy.deepcopy(ORIGINAL_COMPETITIONS)

    # On retourne un faux client HTTP Flask
    return app.test_client()
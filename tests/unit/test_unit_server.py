from datetime import datetime
from server import (
    slugify,
    parse_competition_date,
    is_competition_past,
    validate_booking,
    clubs,
    competitions
)


# Teste que slugify remplace les espaces par des underscores
def test_slugify_replaces_spaces():
    assert slugify("Simply Lift") == "simply_lift"


# Teste que slugify transforme aussi le texte en minuscules
def test_slugify_lowercase():
    assert slugify("SpringFESTIVAL") == "springfestival"


# Teste la conversion d'une date au format ISO
def test_parse_competition_date_iso_format():
    result = parse_competition_date("2027-08-27 10:00:00")
    assert isinstance(result, datetime)


# Teste la conversion d'une date au format français
def test_parse_competition_date_french_format():
    result = parse_competition_date("27/08/2027 10:00:00")
    assert isinstance(result, datetime)


# Teste qu'une date invalide retourne None au lieu de faire planter l'application
def test_parse_competition_date_invalid_format():
    result = parse_competition_date("bad-date")
    assert result is None


# Teste qu'une compétition future n'est pas considérée comme passée
def test_is_competition_past_with_future_date():
    competition = {
        "name": "Future Competition",
        "date": "2099-01-01 10:00:00",
        "numberOfPlaces": "10"
    }

    assert is_competition_past(competition) is False


# Teste qu'une compétition passée est bien considérée comme passée
def test_is_competition_past_with_past_date():
    competition = {
        "name": "Past Competition",
        "date": "2020-01-01 10:00:00",
        "numberOfPlaces": "10"
    }

    assert is_competition_past(competition) is True


# Teste qu'une date invalide rend la compétition non réservable
def test_is_competition_past_with_invalid_date():
    competition = {
        "name": "Invalid Competition",
        "date": "bad-date",
        "numberOfPlaces": "10"
    }

    assert is_competition_past(competition) is True


# Teste la recherche d'un club existant avec next()
def test_find_existing_club_with_next():
    club = next((c for c in clubs if c["email"] == "john@simplylift.co"), None)
    assert club is not None
    assert club["name"] == "Simply Lift"


# Teste qu'un club inconnu retourne None
def test_find_unknown_club_returns_none():
    club = next((c for c in clubs if c["email"] == "fake@test.com"), None)
    assert club is None


# Teste la recherche d'une compétition existante
def test_find_existing_competition_with_next():
    competition = next((c for c in competitions if c["name"] == "Spring Festival"), None)
    assert competition is not None


# Teste une réservation valide
def test_validate_booking_success():
    assert validate_booking(5, 25, 13) is None


# Teste le refus d'une réservation à 0 place
def test_validate_booking_zero_place():
    assert validate_booking(0, 25, 13) == "You must book at least one place."


# Teste le refus d'une réservation de plus de 12 places
def test_validate_booking_more_than_12_places():
    assert validate_booking(13, 25, 13) == "You cannot book more than 12 places."


# Teste le refus si les places disponibles sont insuffisantes
def test_validate_booking_not_enough_places():
    assert validate_booking(10, 5, 13) == "Not enough places available."


# Teste le refus si le club n'a pas assez de points
def test_validate_booking_not_enough_points():
    assert validate_booking(5, 25, 4) == "You do not have enough points."
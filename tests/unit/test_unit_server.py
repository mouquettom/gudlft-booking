from datetime import datetime
from server import (
    slugify,
    parse_competition_date,
    is_competition_past,
    validate_booking,
    find_by,
    find_by_slug,
    loadClubs,
    loadCompetitions
)


# Données de test indépendantes des fichiers JSON
FAKE_CLUBS = [
    {"name": "Test Club", "email": "test@club.com", "points": 10},
    {"name": "Other Club", "email": "other@club.com", "points": 3},
]
FAKE_COMPETITIONS = [
    {"name": "Winter Cup", "date": "2099-01-01 10:00:00",
     "numberOfPlaces": 20},
]


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


# Teste la recherche d'un club par son email
def test_find_by_club_email():
    club = find_by(FAKE_CLUBS, "email", "other@club.com")
    assert club["name"] == "Other Club"


# Teste qu'un club inconnu retourne None
def test_find_by_unknown_club_returns_none():
    assert find_by(FAKE_CLUBS, "email", "fake@test.com") is None


# Teste la recherche d'une compétition par son nom
def test_find_by_competition_name():
    competition = find_by(FAKE_COMPETITIONS, "name", "Winter Cup")
    assert competition["numberOfPlaces"] == 20


# Teste la recherche d'un club à partir du slug de son nom
def test_find_by_slug_club():
    club = find_by_slug(FAKE_CLUBS, "test_club")
    assert club["email"] == "test@club.com"


# Teste qu'un slug inconnu retourne None
def test_find_by_slug_unknown_returns_none():
    assert find_by_slug(FAKE_COMPETITIONS, "fake_competition") is None


# Teste que les points des clubs sont chargés en entiers
def test_load_clubs_converts_points_to_int():
    assert all(isinstance(club["points"], int) for club in loadClubs())


# Teste que les places des compétitions sont chargées en entiers
def test_load_competitions_converts_places_to_int():
    assert all(
        isinstance(competition["numberOfPlaces"], int)
        for competition in loadCompetitions()
    )


# Teste une réservation valide
def test_validate_booking_success():
    assert validate_booking(5, 25, 13) is None


# Teste le refus d'une réservation à 0 place
def test_validate_booking_zero_place():
    assert validate_booking(0, 25, 13) == "You must book at least one place."


# Teste le refus d'une réservation de plus de 12 places
def test_validate_booking_more_than_12_places():
    assert validate_booking(13, 25, 13) == \
        "You cannot book more than 12 places per competition."


# Teste que les places déjà réservées comptent dans la limite de 12
def test_validate_booking_more_than_12_places_in_total():
    assert validate_booking(3, 25, 13, already_booked=10) == \
        "You cannot book more than 12 places per competition."


# Teste qu'on peut compléter une réservation jusqu'à 12 places
def test_validate_booking_up_to_12_places_in_total():
    assert validate_booking(2, 25, 13, already_booked=10) is None


# Teste le refus si les places disponibles sont insuffisantes
def test_validate_booking_not_enough_places():
    assert validate_booking(10, 5, 13) == "Not enough places available."


# Teste le refus si le club n'a pas assez de points
def test_validate_booking_not_enough_points():
    assert validate_booking(5, 25, 4) == "You do not have enough points."
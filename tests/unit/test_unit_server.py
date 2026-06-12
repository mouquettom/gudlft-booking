from datetime import datetime
from server import slugify, parse_competition_date, validate_booking, clubs, competitions


def test_slugify_replaces_spaces():
    assert slugify("Simply Lift") == "simply_lift"


def test_slugify_lowercase():
    assert slugify("Spring Festival") == "spring_festival"


def test_parse_competition_date_iso_format():
    result = parse_competition_date("2027-08-27 10:00:00")
    assert isinstance(result, datetime)


def test_parse_competition_date_french_format():
    result = parse_competition_date("27/08/2027 10:00:00")
    assert isinstance(result, datetime)


def test_parse_competition_date_invalid_format():
    result = parse_competition_date("bad-date")
    assert result is None


def test_find_existing_club_with_next():
    club = next((c for c in clubs if c["email"] == "john@simplylift.co"), None)
    assert club is not None
    assert club["name"] == "Simply Lift"


def test_find_unknown_club_returns_none():
    club = next((c for c in clubs if c["email"] == "fake@test.com"), None)
    assert club is None


def test_find_existing_competition_with_next():
    competition = next((c for c in competitions if c["name"] == "Spring Festival"), None)
    assert competition is not None


def test_validate_booking_success():
    assert validate_booking(5, 25, 13) is None


def test_validate_booking_zero_place():
    assert validate_booking(0, 25, 13) == "You must book at least one place."


def test_validate_booking_more_than_12_places():
    assert validate_booking(13, 25, 13) == "You cannot book more than 12 places."


def test_validate_booking_not_enough_places():
    assert validate_booking(10, 5, 13) == "Not enough places available."


def test_validate_booking_not_enough_points():
    assert validate_booking(5, 25, 4) == "You do not have enough points."
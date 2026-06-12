import server


def test_user_can_login_open_booking_page_and_book(client):
    login_response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"}
    )
    assert login_response.status_code == 200

    booking_response = client.get("/book/spring_festival/simply_lift")
    assert booking_response.status_code == 200
    assert b"How many places" in booking_response.data

    purchase_response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "5"
        }
    )
    assert purchase_response.status_code == 200
    assert b"Great-booking complete!" in purchase_response.data


def test_booking_deducts_points_and_places(client):
    client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "5"
        }
    )

    club = next(c for c in server.clubs if c["name"] == "Simply Lift")
    competition = next(c for c in server.competitions if c["name"] == "Spring Festival")

    assert int(club["points"]) == 8
    assert int(competition["numberOfPlaces"]) == 20


def test_booking_does_not_alter_data_on_failure(client):
    client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Iron Temple",
            "places": "5"
        }
    )

    club = next(c for c in server.clubs if c["name"] == "Iron Temple")
    competition = next(c for c in server.competitions if c["name"] == "Spring Festival")

    assert int(club["points"]) == 4
    assert int(competition["numberOfPlaces"]) == 25


def test_user_cannot_book_zero_place(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "0"
        }
    )
    assert response.status_code == 200
    assert b"You must book at least one place" in response.data


def test_user_cannot_book_more_than_12_places(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "13"
        }
    )
    assert response.status_code == 200
    assert b"You cannot book more than 12 places" in response.data


def test_user_cannot_book_without_enough_points(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Iron Temple",
            "places": "5"
        }
    )
    assert response.status_code == 200
    assert b"You do not have enough points" in response.data


def test_points_board_visible_without_login(client):
    response = client.get("/points")
    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data
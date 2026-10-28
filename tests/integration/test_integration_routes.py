# Teste que la page d'accueil répond correctement
def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the" in response.data


# Teste la route /showSummary avec un email valide
def test_login_valid_email(client):
    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"}
    )

    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Competitions" in response.data


# Teste qu'un email invalide redirige vers l'accueil avec un message d'erreur
def test_login_invalid_email_redirects(client):
    response = client.post(
        "/showSummary",
        data={"email": "fake@test.com"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Email not found" in response.data


# Teste que la page publique des points affiche les clubs
def test_points_page_displays_clubs(client):
    response = client.get("/points")

    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data


# Teste que la page de réservation s'affiche avec une compétition et un club valides
def test_book_page_valid_data(client):
    response = client.get("/book/spring_festival/simply_lift")

    assert response.status_code == 200
    assert b"Spring Festival" in response.data
    assert b"How many places" in response.data


# Teste qu'une compétition invalide ne fait pas planter l'application
def test_book_page_invalid_competition_redirects(client):
    response = client.get(
        "/book/fake_competition/simply_lift",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Something went wrong" in response.data


# Teste qu'on ne peut pas ouvrir la réservation d'une compétition passée
def test_book_page_past_competition_is_refused(client):
    response = client.get("/book/summer_open/simply_lift")

    assert response.status_code == 200
    assert b"This competition has already taken place" in response.data
    assert b"How many places" not in response.data


# Teste qu'une réservation avec un club inconnu redirige vers l'accueil
def test_purchase_unknown_club_redirects(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Fake Club",
            "places": "1"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Competition or club not found" in response.data


# Teste qu'un nombre de places non numérique est refusé proprement
def test_purchase_invalid_number_of_places(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "abc"
        }
    )

    assert response.status_code == 200
    assert b"Invalid number of places" in response.data


# Teste que la déconnexion ramène vers l'accueil
def test_logout_redirects_home(client):
    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome to the" in response.data
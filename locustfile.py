"""
Tests de performance avec Locust.
Objectif : ≤ 5s pour les listes, ≤ 2s pour les mises à jour.
6 utilisateurs par défaut (spécification).

Lancement : locust -f locustfile.py --host=http://127.0.0.1:5000

Les données sont gardées en mémoire par le serveur : les réservations
faites pendant un test s'accumulent. Redémarrer le serveur avant chaque
test pour repartir des données initiales.
"""
from itertools import cycle

from locust import HttpUser, task, between


# Clubs de clubs.json : chaque utilisateur simulé reçoit le suivant
CLUBS = cycle([
    {"email": "john@simplylift.co", "name": "Simply Lift",
     "slug": "simply_lift"},
    {"email": "admin@irontemple.com", "name": "Iron Temple",
     "slug": "iron_temple"},
    {"email": "kate@shelifts.co.uk", "name": "She Lifts",
     "slug": "she_lifts"},
])


class GudlftUser(HttpUser):
    """ Simule un secrétaire de club utilisant l'application. """

    wait_time = between(1, 3)

    # Compétition à venir sur laquelle les réservations sont faites
    COMPETITION = "Spring Festival"
    COMPETITION_SLUG = "spring_festival"

    def on_start(self):
        """
        Choisit le club de l'utilisateur puis se connecte une fois.
        Les tâches suivantes réutilisent la session HTTP (cookies).
        """
        self.club = next(CLUBS)
        self.client.post("/showSummary", data={"email": self.club["email"]})

    @task(3)
    def view_show_summary_page(self):
        """ Consulter sa page d'accueil (liste des compétitions). """
        self.client.post("/showSummary", data={"email": self.club["email"]})

    @task(2)
    def view_booking_page(self):
        """ Accéder à la page de réservation d'une compétition. """
        self.client.get(
            f"/book/{self.COMPETITION_SLUG}/{self.club['slug']}",
            # Regroupe les URLs dans le rapport
            name="/book/[competition]/[club]"
        )

    @task(1)
    def purchasePlaces(self):
        """ Réserver une place — mise à jour, doit rester ≤ 2s. """
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": self.COMPETITION,
                "club": self.club["name"],
                "places": "1"
            }
        )

    @task(2)
    def view_points_board(self):
        """ Consulter le tableau public des points — doit rester ≤ 5s. """
        self.client.get("/points")

    @task(1)
    def logout_and_relogin(self):
        """ Déconnexion puis reconnexion pour simuler un cycle complet. """
        self.client.get("/logout")
        self.client.post("/showSummary", data={"email": self.club["email"]})

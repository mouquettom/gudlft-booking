"""
Tests de performance avec Locust.
Objectif : ≤ 5s pour les listes, ≤ 2s pour les mises à jour.
6 utilisateurs par défaut (spécification).

Lancement : locust -f locustfile.py --host=http://localhost:5000
"""
from locust import HttpUser, task, between


class GudlftUser(HttpUser):
    """ Simule un secrétaire de club utilisant l'application. """

    wait_time = between(1, 3)

    # Données de test représentatives d'un vrai utilisateur
    EMAIL = "john@simplylift.co"
    CLUB = "Simply Lift"
    COMPETITION = "Spring Festival"
    COMPETITION_SLUG = "spring_festival"
    CLUB_SLUG = "simply_lift"

    def on_start(self):
        """
        Connexion initiale : une seule fois au démarrage de la session.
        Les tâches suivantes réutilisent la session HTTP (cookies).
        """
        self.client.post("/showSummary", data={"email": self.EMAIL})

    @task(3)
    def view_show_summary_page(self):
        """ Consulter sa page d'accueil après connexion (liste des compétitions). """
        self.client.post("/showSummary", data={"email": self.EMAIL})

    @task(2)
    def view_booking_page(self):
        """ Accéder à la page de réservation d'une compétition. """
        self.client.get(
            f"/book/{self.COMPETITION_SLUG}/{self.CLUB_SLUG}",
            name="/book/[competition]/[club]"  # regroupe les URLs dans le rapport
        )

    @task(1)
    def purchasePlaces(self):
        """ Réserver des places — action de mise à jour, doit rester ≤ 2s. """
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": self.COMPETITION,
                "club": self.CLUB,
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
        self.client.post("/showSummary", data={"email": self.EMAIL})
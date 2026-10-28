import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


# Charge les clubs depuis clubs.json
# Les points sont convertis en entiers une fois pour toutes
def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
    for club in listOfClubs:
        club['points'] = int(club['points'])
    return listOfClubs


# Charge les compétitions depuis competitions.json
# Le nombre de places est converti en entier une fois pour toutes
def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
    for competition in listOfCompetitions:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])
    return listOfCompetitions


# Transforme un nom en slug compatible URL
# Exemple : "Spring Festival" -> "spring_festival"
def slugify(value):
    return value.replace(' ', '_').lower()


# Recherche le premier élément (club ou compétition) dont le champ `key`
# vaut `value`. Renvoie None si aucun élément ne correspond.
# Exemple : find_by(clubs, 'email', 'john@simplylift.co')
def find_by(items, key, value):
    return next((item for item in items if item[key] == value), None)


# Recherche un élément (club ou compétition) à partir du slug de son nom
# Exemple : find_by_slug(competitions, 'spring_festival')
def find_by_slug(items, slug):
    return next(
        (item for item in items if slugify(item['name']) == slug),
        None
    )


# Convertit une date texte en objet datetime Python
def parse_competition_date(date_value):
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
    ]

    # On teste plusieurs formats possibles
    for date_format in formats:
        try:
            return datetime.strptime(date_value, date_format)
        except ValueError:
            continue

    # Si aucun format ne fonctionne, on retourne None
    return None


# Vérifie si une compétition est déjà passée
def is_competition_past(competition):
    date = parse_competition_date(competition['date'])

    # Si la date est invalide, on considère la compétition comme non réservable
    if date is None:
        return True

    return date < datetime.now()


# Nombre maximum de places qu'un club peut réserver sur une compétition
MAX_PLACES_PER_COMPETITION = 12


# Vérifie les règles métier d'une réservation
# already_booked : places déjà réservées par ce club sur cette compétition
def validate_booking(places_required, available_places, club_points,
                     already_booked=0):
    if places_required <= 0:
        return 'You must book at least one place.'
    if already_booked + places_required > MAX_PLACES_PER_COMPETITION:
        return 'You cannot book more than 12 places per competition.'
    if places_required > available_places:
        return 'Not enough places available.'
    if places_required > club_points:
        return 'You do not have enough points.'

    # None signifie : aucune erreur
    return None


# Création de l'application Flask
app = Flask(__name__)

# Nécessaire pour utiliser flash()
app.secret_key = 'something_special'


# Les fichiers JSON sont chargés une fois au lancement du serveur
competitions = loadCompetitions()
clubs = loadClubs()

# Places déjà réservées, par couple (nom du club, nom de la compétition)
# Exemple : {("Simply Lift", "Spring Festival"): 5}
bookings = {}


# Renvoie le nombre de places déjà réservées par un club sur une compétition
def booked_places(club_name, competition_name):
    return bookings.get((club_name, competition_name), 0)


# Rend booked_places() et le filtre slugify utilisables dans les templates
app.jinja_env.globals['booked_places'] = booked_places
app.add_template_filter(slugify)


# Route d'accueil
@app.route('/')
def index():
    return render_template('index.html')


# Route de connexion du secrétaire
@app.route('/showSummary', methods=['POST'])
def login():
    email = request.form.get('email')

    # Recherche sécurisée du club correspondant à l'email
    club = find_by(clubs, 'email', email)

    # Si aucun club n'est trouvé, on affiche une erreur
    if not club:
        flash("Email not found. Please try again.")
        return redirect(url_for('index'))

    # Sinon, on affiche la page récapitulative du club
    return render_template('showSummary.html', club=club, competitions=competitions)


# Route affichant la page de réservation
@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = find_by_slug(clubs, club)
    foundCompetition = find_by_slug(competitions, competition)

    # Si le club ou la compétition n'existe pas, on évite le crash
    if not foundClub or not foundCompetition:
        flash("Something went wrong — please try again.")
        return redirect(url_for('index'))

    # On empêche la réservation d'une compétition passée
    if is_competition_past(foundCompetition):
        flash("This competition has already taken place.")
        return render_template(
            'showSummary.html',
            club=foundClub,
            competitions=competitions
        )

    # Si tout est correct, on affiche booking.html
    return render_template(
        'booking.html',
        club=foundClub,
        competition=foundCompetition
    )


# Route qui traite la réservation
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form.get('competition')
    club_name = request.form.get('club')
    places = request.form.get('places')

    # Recherche de la compétition et du club
    competition = find_by(competitions, 'name', competition_name)
    club = find_by(clubs, 'name', club_name)

    # Sécurité : si les données envoyées sont incorrectes
    if not competition or not club:
        flash("Competition or club not found.")
        return redirect(url_for('index'))

    # Conversion du nombre de places en entier
    try:
        placesRequired = int(places)
    except (TypeError, ValueError):
        flash("Invalid number of places.")
        return render_template(
            'booking.html',
            club=club,
            competition=competition,
        )

    availablePlaces = competition['numberOfPlaces']
    clubPoints = club['points']
    alreadyBooked = booked_places(club['name'], competition['name'])

    # Vérification des règles métier
    error = validate_booking(
        placesRequired, availablePlaces, clubPoints, alreadyBooked
    )

    if error:
        flash(error)
        return render_template('booking.html', club=club, competition=competition)

    # Si la réservation est valide, on met à jour les données en mémoire
    competition['numberOfPlaces'] = availablePlaces - placesRequired
    club['points'] = clubPoints - placesRequired
    bookings[(club['name'], competition['name'])] = (
        alreadyBooked + placesRequired
    )

    flash('Great-booking complete!')

    return render_template('showSummary.html', club=club, competitions=competitions)


# Page publique des points
@app.route('/points')
def displayPoints():
    return render_template('displayPoints.html', clubs=clubs)


# Déconnexion simple : retour accueil
@app.route('/logout')
def logout():
    return redirect(url_for('index'))


# Permet de lancer l'application avec : python server.py
if __name__ == '__main__':
    app.run()

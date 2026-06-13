import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


# Charge les clubs depuis clubs.json
def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


# Charge les compétitions depuis competitions.json
def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


# Transforme un nom en slug compatible URL
# Exemple : "Spring Festival" -> "spring_festival"
def slugify(value):
    return value.replace(' ', '_').lower()


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


# Vérifie les règles métier d'une réservation
def validate_booking(places_required, available_places, club_points):
    if places_required <= 0:
        return 'You must book at least one place.'
    if places_required > 12:
        return 'You cannot book more than 12 places.'
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


# Route d'accueil
@app.route('/')
def index():
    return render_template('index.html')


# Route de connexion du secrétaire
@app.route('/showSummary', methods=['POST'])
def login():
    email = request.form.get('email')

    # Recherche sécurisée du club correspondant à l'email
    club = next((c for c in clubs if c['email'] == email), None)

    # Si aucun club n'est trouvé, on affiche une erreur
    if not club:
        flash("Email not found. Please try again.")
        return redirect(url_for('index'))

    # Sinon, on affiche la page récapitulative du club
    return render_template('showSummary.html', club=club, competitions=competitions)


# Route affichant la page de réservation
@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next(
        (c for c in clubs if slugify(c['name']) == club),
        None
    )

    foundCompetition = next(
        (comp for comp in competitions if slugify(comp['name']) == competition),
        None
    )

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

    # Recherche de la compétition
    competition = next(
        (comp for comp in competitions if comp['name'] == competition_name),
        None
    )

    # Recherche du club
    club = next(
        (c for c in clubs if c['name'] == club_name),
        None
    )

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

    availablePlaces = int(competition['numberOfPlaces'])
    clubPoints = int(club['points'])

    # Vérification des règles métier
    error = validate_booking(placesRequired, availablePlaces, clubPoints)

    if error:
        flash(error)
        return render_template('booking.html', club=club, competition=competition)

    # Si la réservation est valide, on met à jour les données en mémoire
    competition['numberOfPlaces'] = availablePlaces - placesRequired
    club['points'] = clubPoints - placesRequired

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
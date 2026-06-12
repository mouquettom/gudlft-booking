import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']


def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


def slugify(value):
    return value.replace(' ', '_').lower()


def parse_competition_date(date_value):
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
    ]

    for date_format in formats:
        try:
            return datetime.strptime(date_value, date_format)
        except ValueError:
            continue

    return None


def is_competition_past(competition):
    """Retourne True si la compétition est déjà passée."""
    date = parse_competition_date(competition['date'])

    if date is None:
        return True

    return date < datetime.now()


def validate_booking(places_required, available_places, club_points):
    """
    Valide une demande de réservation.
    Retourne un message d'erreur (str) ou None si tout est valide.
    """
    if places_required <= 0:
        return 'You must book at least one place.'
    if places_required > 12:
        return 'You cannot book more than 12 places.'
    if places_required > available_places:
        return 'Not enough places available.'
    if places_required > club_points:
        return 'You do not have enough points.'

    return None


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def login():
    email = request.form.get('email')

    club = next((c for c in clubs if c['email'] == email), None)

    if not club:
        flash("Email not found. Please try again.")
        return redirect(url_for('index'))

    return render_template('showSummary.html', club=club, competitions=competitions)


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

    if not foundClub or not foundCompetition:
        flash("Something went wrong — please try again.")
        return redirect(url_for('index'))

    if is_competition_past(foundCompetition):
        flash("This competition has already taken place.")
        return render_template(
            'showSummary.html',
            club=foundClub,
            competitions=competitions
        )

    return render_template(
        'booking.html',
        club=foundClub,
        competition=foundCompetition
    )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form.get('competition')
    club_name = request.form.get('club')
    places = request.form.get('places')

    competition = next(
        (c for c in competitions if c['name'] == competition_name),
        None
    )

    club = next(
        (c for c in clubs if c['name'] == club_name),
        None
    )

    if not competition or not club:
        flash("Competition or club not found.")
        return redirect(url_for('index'))

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

    error = validate_booking(placesRequired, availablePlaces, clubPoints)
    if error:
        flash(error)
        return render_template('booking.html', club=club, competition=competition)

    competition['numberOfPlaces'] = availablePlaces - placesRequired
    club['points'] = clubPoints - placesRequired

    flash('Great-booking complete!')
    return render_template('showSummary.html', club=club, competitions=competitions)


@app.route('/points')
def displayPoints():
    return render_template('displayPoints.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
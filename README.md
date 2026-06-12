# GÜDLFT – Club Competition Booking Platform

## Description

GÜDLFT est une application web développée avec Flask permettant aux clubs sportifs 
de réserver des places pour des compétitions.

L'objectif principal est d'améliorer la qualité du code existant, corriger les bugs 
identifiés, ajouter de nouvelles fonctionnalités, mettre en place une stratégie de 
tests complète et effectuer des tests de performance.

---

## Fonctionnalités

### Authentification

- Connexion d'un club via son adresse email
- Gestion des erreurs en cas d'email inconnu

### Réservation de compétitions

- Consultation des compétitions disponibles
- Réservation de places
- Déduction automatique des points du club
- Déduction automatique du nombre de places restantes

### Règles métier

- Impossible de réserver une compétition passée
- Maximum 12 places réservables par compétition
- Impossible de réserver plus de places que disponibles
- Impossible de réserver plus de places que le nombre de points du club

### Affichage des points

- Consultation publique des points de tous les clubs

---

## Technologies utilisées

- Python 3
- Flask
- Pytest
- Coverage
- Locust
- HTML5
- CSS3

---

## Structure du projet

```text
GUDLFT/
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── showSummary.html
│   ├── booking.html
│   └── displayPoints.html
│
├── tests/
│   ├── functional/
│   │   └── test_functional_user.py
│   │
│   ├── integration/
│   │   └── test_integration_routes.py
│   │
│   ├── unit/
│   │   └── test_unit_server.py
│   │
│   └── conftest.py
│
├── clubs.json
├── competitions.json
├── locustfile.py
├── requirements.txt
├── server.py
└── README.md
```

---

## Installation

### Cloner le projet

```bash
git clone git@github.com:mouquettom/GUDLFT-TESTS.git
cd GUDLFT-TESTS
```

### Créer un environnement virtuel

```bash
python -m venv .env
```

### Activer l'environnement

Mac / Linux :

```bash
source .env/bin/activate
```

Windows :

```bash
.env\Scripts\activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Lancement de l'application

```bash
python server.py
```

ou

```bash
flask run
```

L'application sera accessible à l'adresse :

```text
http://127.0.0.1:5000
```

---

## Exécution des tests

### Lancer tous les tests

```bash
pytest
```

### Lancer les tests avec couverture

```bash
coverage run -m pytest
coverage report
```

### Générer un rapport HTML

```bash
coverage html
```

Puis ouvrir :

```text
htmlcov/index.html
```

---

## Types de tests implémentés

### Tests unitaires

Validation des fonctions métier :

- slugify()
- parse_competition_date()
- validate_booking()
- recherche des clubs
- recherche des compétitions

### Tests d'intégration

Validation :

- des routes Flask
- des templates
- des réponses HTTP
- des messages d'erreur

### Tests fonctionnels

Validation de parcours utilisateur complets :

- connexion
- réservation
- déduction des points
- gestion des erreurs

---

## Tests de performance

Le projet utilise Locust pour les tests de charge.

### Lancer le serveur Flask

```bash
python server.py
```

### Lancer Locust

```bash
locust -f locustfile.py --host=http://127.0.0.1:5000
```

Ouvrir ensuite :

```text
http://localhost:8089
```

Paramètres recommandés :

```text
Users : 6
Spawn Rate : 1
```

### Objectifs de performance

- Pages de consultation : < 5 secondes
- Opérations de réservation : < 2 secondes

---

## Bugs corrigés

### Bug #1

Connexion avec un email inconnu provoquant une erreur.

### Bug #2

Réservation possible malgré un nombre insuffisant de points.

### Bug #3

Réservation possible sur une compétition passée.

### Bug #4

Réservation de plus de 12 places autorisée.

---

## Auteur

@tom_mouquet

Projet réalisé dans le cadre de la formation OpenClassrooms.
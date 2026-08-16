# GÜDLFT Booking

## Description

GÜDLFT is a web application built with Flask that allows sports clubs to
book spots for competitions.

The main objective of this project is to improve the quality of the
existing codebase, fix identified bugs, add new features, implement a
comprehensive testing strategy, and perform performance testing.

------------------------------------------------------------------------

## Features

### Authentication

-   Club login using an email address
-   Error handling for unknown email addresses

### Competition Booking

-   View available competitions
-   Book spots for competitions
-   Automatic deduction of club points
-   Automatic deduction of remaining competition spots

### Business Rules

-   Past competitions cannot be booked
-   Maximum of 12 spots per booking
-   Cannot book more spots than are available
-   Cannot book more spots than the club's available points

### Points Display

-   Public access to the points balance of all clubs

------------------------------------------------------------------------

## Technologies Used

-   Python 3
-   Flask
-   Pytest
-   Coverage
-   Locust
-   HTML5
-   CSS3

------------------------------------------------------------------------

## Project Structure

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
    │   ├── integration/
    │   │   └── test_integration_routes.py
    │   ├── unit/
    │   │   └── test_unit_server.py
    │   └── conftest.py
    │
    ├── clubs.json
    ├── competitions.json
    ├── locustfile.py
    ├── requirements.txt
    ├── server.py
    └── README.md

------------------------------------------------------------------------

## Installation

### Clone the Repository

``` bash
git clone git@github.com:mouquettom/gudlft-booking.git
cd gudlft-booking
```

### Create a Virtual Environment

``` bash
python -m venv .env
```

### Activate the Virtual Environment

Mac / Linux:

``` bash
source .env/bin/activate
```

Windows:

``` bash
.env\Scripts\activate
```

### Install Dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Running the Application

``` bash
python server.py
```

or

``` bash
flask run
```

The application will be available at:

    http://127.0.0.1:5000

------------------------------------------------------------------------

## Running the Tests

### Run All Tests

``` bash
pytest
```

### Run Tests with Coverage

``` bash
coverage run -m pytest
coverage report
```

### Generate an HTML Coverage Report

``` bash
coverage html
```

Then open:

    htmlcov/index.html

------------------------------------------------------------------------

## Implemented Test Types

### Unit Tests

Validation of business logic functions:

-   `slugify()`
-   `parse_competition_date()`
-   `validate_booking()`
-   Club lookup
-   Competition lookup

### Integration Tests

Validation of:

-   Flask routes
-   Templates
-   HTTP responses
-   Error messages

### Functional Tests

Validation of complete user workflows:

-   Login
-   Booking
-   Points deduction
-   Error handling

------------------------------------------------------------------------

## Performance Testing

The project uses Locust for load testing.

### Start the Flask Server

``` bash
python server.py
```

### Start Locust

``` bash
locust -f locustfile.py --host=http://127.0.0.1:5000
```

Then open:

    http://localhost:8089

Recommended parameters:

    Users: 6
    Spawn Rate: 1

### Performance Objectives

-   Browsing pages: \< 5 seconds
-   Booking operations: \< 2 seconds

------------------------------------------------------------------------

## Fixed Bugs

### Bug #1

Logging in with an unknown email address caused an error.

### Bug #2

Bookings were possible even when the club had insufficient points.

### Bug #3

Bookings were possible for past competitions.

### Bug #4

Booking more than 12 spots was allowed.

------------------------------------------------------------------------

## Author

@tom_mouquet

Project developed as part of the OpenClassrooms **Développeur
d'application Python** training program.

## Superheros API

## How to get started

Ensure you have python, pipenv and sqlite3 installed locally:

```bash
python3 --version
pipenv --version
sqlite3 --version
```

Else you can install them:

```bash
sudo apt install pipenv
sudo apt install sqlite3
```

1. Clone the repo locally and cd into it:

```bash
git clone https://github.com/Prince-gk/Superheroes.git && cd Superheroes
```

2. Initialize the virtual environment and setup database (sqlite):

```bash
pipenv shell # activate a virtual environment
pipenv install # install the dependecies required
```

Setup the DB:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

Seed the database:

```bash
pipenv run python -m app.seed
```

On your terminal:

```bash
source .env
flask run
```

## Structure

```bash
.
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── seed.py
├── config.py
├── instance
│   └── app.db
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── cf7302562520_initial_migration.py
├── Pipfile
├── Pipfile.lock
├── README.md
└── run.py

5 directories, 15 files

```

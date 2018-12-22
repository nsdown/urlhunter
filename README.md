# URL Hunter

URL is a kind of resource.

## Quick Start

### Build

``` bash
git clone https://github.com/alphardex/urlhunter
cd urlhunter
pipenv install --dev
pipenv shell
```

### Database Migration

``` bash
flask db init
flask db migrate
flask db upgrade
```

### Run

``` bash
flask run
```

### Test Coverage

``` bash
pipenv run coverage
```

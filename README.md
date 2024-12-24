# MicroLoan Managment System

```
MicroLoan managment system backend service developed with Django and DRF(DjangoRestFramework)
Features
User Authorization and Authentication
Loan Request
Loan Review and status managment
```

### Project Requirements

- Python 3.10.x

### Project Setup

#### Create virtual environment

```
pip install virtualenv
virtualenve {virtualenv_name}
Linux
{virtualenv_name}\bin\activate
Windows
{virtualenv_name}\Scripts\activate
```

#### Install Requirements

```
pip install -r requirements.txt
```

#### Run Migrations

```
Linux
python3 manage.py migrate
Windows
python manage.py migrate
```

#### Run Server

##### Linux

```
python3 manage.py runserver
# you can set your desired port by running
python manage.py runserver 0.0.0.0:{PORT_NUMBER}
```

##### Windows

```
python manage.py runserver
or
py manage.py runserver
# you can set your desired port by running
python manage.py runserver 0.0.0.0:{PORT_NUMBER}
```

#### Run Server

```
API Authorization is JWT Token
access documented API at http://127.0.0.1:{PORT_NUMER}
```

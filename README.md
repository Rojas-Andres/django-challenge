# Stack for Django Projects by Andres Rojas





#### Validaciones


### Prestamos (loan)
	- Cuando se crea un prestamo el valor del amount como el valor de outstanding es el mismo porque como tal el prestamo ha sido creado y no se ha abonado nada.
	- El prestamo no puede ser modificado luego que se cambie a active.
	- El amount de prestamo no puede exceder el score de customer.
	- El amount no puede ser negativo
	- El prestamo cuando se crea por defecto se crea en pending , no se considera crear en activo porque generalmente cuando son pagos van a un webhook y este deuvelve si el pago se hizo correctamente o no, tampoco se coloco en rejected porque para que crear un prestamo si ya esta rechazado.


	Update:
		- No se puede modificar un prestamo ya activo ni rechazado , esto con el fin de no modificar el amount de un prestamo cuando ya se activo
###  Payments
# Creacion de pagos json - POST - /api/payments/
{
    "payment_detail": [
        {
            "amount":2222,
            "load_external_id":"121331113"
        }
    ],
    "payment":{
        "external_id":"11111",
        "customer_external_id":"213asdx"
    }
}

- Lo decidi hacer asi porque en el requerimiento se indica que un pago puede ser para muchos prestamos por lo tanto el payment_detail tiene el amount de ese prestamo
    - Validaciones
        - Solo se permite abonar a un prestamo que esta activo
        - El amount de cada prestamo no puede ser mayor al outstanding porque no se puede pagar mas que el prestamo mismo
        - El load_external_id debe de existir en la tabla de prestamos en external_id
        - El payment -> external_id debe de ser unico.
        - Por defecto un pago es activado, en el caso de que se rechace un pago los outsading vuelven a su valor original. La API:
             - /api/payments/?external_id=3131 -> PATCH
                - Esta api solo recibe el external_id del pago como query param.

- Consideraciones:
    - El status del pago deberia de ser pending, rejected y activo . En la prueba tecnica solo esta rejected y activo, pero generalmente el pago esta en pendiente y luego se activa o se rechaza. El funcionamiento actual es que cuando se crea el pago por defecto esta en activo. Por lo tanto hay otra api para actualizar el pago a rechazado y cuando se rechaza un pago los outsading de ese pago vuelven a ser su valor original
## Features

- Swagger and postman are used for documentation

## Requirements

- Docker
- docker-compose

## Run

### Setup

1. Clone repository:

- `git clone git@github.com:Rojas-Andres/django_stack.git`
- `cd django_stack`

### Run With Docker

2. Copy `.env.example` to `.env` and custom:

- `cp .env.example .env`

3. docker-compose

- `docker-compose -f docker-compose.dev.yml build`
- `docker-compose -f docker-compose.dev.yml up`

### Run With Virtualenv

1. Copy `.env.example` to `.env` and custom:

- `cp .env.example .env`

1. Create virtualenv and activate

- `python -m venv venv`
- `source venv/bin/activate` _(Linux)_
- `./venv/Scripts/activate` _(Windows)_

4. Install requirements

- `pip install -r /requirements.txt`

1. Run

- `cd src`
- `python manage.py runserver`

## Migrations With Docker

### With Docker

- `docker-compose -f docker-compose.dev.yml run --rm django sh -c "python manage.py makemigrations"`
- `docker-compose -f docker-compose.dev.yml run --rm django sh -c "python manage.py migrate"`

### With Virtualenv

- `cd src`
- `python manage.py makemigrations`
- `python manage.py migrate`

## Create new app

### With Docker

- `docker-compose -f docker-compose.dev.yml run --rm django sh -c "python manage.py startapp appname"`

### With Virtualenv

- `cd src`
- `python manage.py startapp appname`

## Test

### With Docker

- `docker-compose -f docker-compose.dev.yml run --rm django sh -c "python manage.py test"`

### With Virtualenv

- `cd src`
- `python manage.py test`

## Test coverage

### With Docker

- `docker-compose -f docker-compose.local.yml run --rm django sh -c "coverage run --source=. manage.py test --noinput"`

To see the report:

- `docker-compose -f docker-compose.local.yml run --rm django sh -c "coverage report"`

To generate html report:

- `docker-compose -f docker-compose.local.yml run --rm django sh -c "coverage html"`

### With Virtualenv

- `cd src`
- `coverage run --source=. manage.py test --noinput`

To see the report:

- `coverage report`

To generate html report:

- `coverage html`

## Linter

Use pre-commit to run linter before commit, the command is:

- `pre-commit run --all-files`

## Docker build local
` docker build --no-cache -t stack_django . `
` docker run -p 8000:8000 stack_django `

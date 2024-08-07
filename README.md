# Challange by Andres Rojas


## Patrones de diseño usados

#### Creacion de customers
- Para procesar y crear clientes, se utiliza una fábrica que selecciona la estrategia adecuada basada en el tipo de procesamiento solicitado. Esto evita el uso de múltiples sentencias if y facilita la extensión del sistema. La fábrica se implementa mediante la clase ProcessingFactory, que utiliza un mapa (strategy_map_processing) para asociar nombres de estrategias con sus respectivas implementaciones.

- Uso del Patrón Factory

El patrón Factory se implementa mediante la clase ProcessingFactory, que proporciona métodos para obtener y ejecutar la estrategia de procesamiento adecuada.
Explicación del Mapa de Estrategias

El mapa strategy_map_processing asocia nombres de estrategias (json, txt) con instancias de las clases que implementan esas estrategias (JsonProcessing, TxtProcessing). Esto permite seleccionar y ejecutar la estrategia adecuada sin necesidad de múltiples sentencias if.

#### Cumplimiento de los Principios SOLID

- Single Responsibility Principle (SRP): La clase ProcessingFactory tiene una única responsabilidad: seleccionar y ejecutar la estrategia de procesamiento adecuada.

- Open/Closed Principle (OCP): El sistema está abierto a la extensión pero cerrado a la modificación. Si se necesita añadir una nueva estrategia de procesamiento (por ejemplo, CSV, XLS), se puede añadir una nueva entrada al mapa strategy_map_processing sin modificar el código existente.

- Liskov Substitution Principle (LSP): Las estrategias (JsonProcessing, TxtProcessing) pueden sustituir a la interfaz ProcessingStrategy sin alterar el comportamiento del programa.

- Interface Segregation Principle (ISP): La interfaz ProcessingStrategy es específica y no obliga a las clases que la implementan a depender de métodos que no utilizan.

- Dependency Inversion Principle (DIP): El código depende de abstracciones (ProcessingStrategy) y no de implementaciones concretas.


#### Prestamos (loan)
	- Cuando se crea un prestamo el valor del amount como el valor de outstanding es el mismo porque como tal el prestamo ha sido creado y no se ha abonado nada.
	- El prestamo no puede ser modificado luego que se cambie a active.
	- El amount de prestamo no puede exceder el score de customer.
	- El amount no puede ser negativo
	- El prestamo cuando se crea por defecto se crea en pending , no se considera crear en activo porque generalmente cuando son pagos van a un webhook y este deuvelve si el pago se hizo correctamente o no, tampoco se coloco en rejected porque para que crear un prestamo si ya esta rechazado.


	Update:
		- No se puede modificar un prestamo ya activo ni rechazado , esto con el fin de no modificar el amount de un prestamo cuando ya se activo

####  Payments
##### Creacion de pagos json - POST - /api/payments/
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


### Filters para peticiones tipo GET
- En caso de las peticiones tipo get implemente una vista generica que contiene todo lo necesario para el filtrado la cual es ViewTemplateFilters, esta vista ya tiene integrado la paginacion, los query_param y en el caso de tener un filter personalizado solo seria colocarlo en cada vista que requiera el tipo get. En cada aplicacion que realice filters se encuentra un archivo filters que hace referencia a ese tipo de filtrado en especifico de esa api.


## Features

- Swagger and postman are used for documentation

## correr proyecto

### Setup

1. Clone repository:

- `git clone git@github.com:Rojas-Andres/django-challenge.git`
- `cd django-challenge`

2. Copy `.env.example` to `.env` and custom:

- `cp .env.example .env`


### Correr proyecto con docker (recordar crear el .env en la raiz)
- ` docker-compose -f docker-compose.dev.yml build `
- ` docker-compose -f docker-compose.dev.yml up `

![](images/local_env/docker_compose_local_run.png)

### Validaciones github actions , pre-commit -> coverage -> deploy

#### Validacion pre-commit
![](images/github_actions_validation/pre-commit-validate-github.png)

#### Validacion coverage
![](images/github_actions_validation/testing-coverage-github.png)


#### Total de test ejecutados
![](images/github_actions_validation/total_Test.png)


#### Validacion deploy ecs fargate
![](images/github_actions_validation/github-actions-deploy-django-ecs-fargate.png)

#### Validacion validaciones success

- Las validaciones se pueden ver en actions de github
![](images/github_actions_validation/success_pipeline.png)



#### Deployment en ECS fargate

- Se despliega el cluster de ecs, la definicion de tarea
![](images/deployment_cdk/task_run_success.png)

- Se ejecuta la tarea donde esta la aplicacion de django
![](images/deployment_cdk/task_run.png)

- Registros de la tarea
![](images/deployment_cdk/records_task.png)


- Despliegue del Load balancer
![](images/deployment_cdk/load_balancer.png)

http://django-lb8a1-dmkffoleebi1-1056492271.us-east-2.elb.amazonaws.com:8000/

![](images/deployment_cdk/show_healtcheck.png)

- Swagger Inteface
    - Personalmente el swagger de django no me gusta pero aca lo dejo aunque faltaria mejorarlo en terminos de query params. Prefiero usar postman aunque toca agregar api por api.
![](images/deployment_cdk/swagger_interface.png)


## Deployment domain

- Domain https://develop.andres-rojas-l.live/

![](images/domain_deploy/domain_deploy.png)

- Login user domain

![](images/domain_deploy/login_user_domain.png)
https://develop.andres-rojas-l.live/api/auth/login/
{
    "email":"andresrojas@gmail.com",
    "password":"123456"
}


- Recordar que el resto de apis estan protegidas entonces se debe de pasar el Bearer Token obtenido del login


### Run With Virtualenv

1. Create virtualenv and activate

- `python -m venv venv`
- `source venv/bin/activate` _(Linux)_
- `./venv/Scripts/activate` _(Windows)_

2. Install requirements

- `pip install -r /requirements/local.txt`

3. Run

- `cd src`
- `python manage.py runserver`

####  Test

### Pruebas unitarias con entorno virtual

- `cd src`
- `python manage.py test`

### Pruebas unitarias con docker-compose

- `docker-compose -f docker-compose.testing.yml run --rm django sh -c "coverage run --source=. manage.py test --noinput"`

- Para ver el reporte del coverage:

- `docker-compose -f docker-compose.testing.yml run --rm django sh -c "coverage report"`

Generar el reporte en HTML:

- `docker-compose -f docker-compose.testing.yml run --rm django sh -c "coverage html"`


![](images/local_env/testing_local.png)

### Testing con el entorno virtual

- `cd src`
- `coverage run --source=. manage.py test --noinput`

To see the report:

- `coverage report`

To generate html report:

- `coverage html`


## Linter para la validacion de codigo

Use pre-commit to run linter before commit, the command is:

- `pre-commit run --all-files`

### Consideraciones

## Docker build ECR and push
- login
    - aws ecr-public get-login-password --region us-east-1 --profile pheno | docker login --username AWS --password-stdin public.ecr.aws
- docker build -t ecr_template:v1 -f ecr.Dockerfile .
- docker tag ecr_template:v1 public.ecr.aws/f5k9u7m7/ecr_template_python_fargate:latest
- docker push public.ecr.aws/f5k9u7m7/ecr_template_python_fargate:latest

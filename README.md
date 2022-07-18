# Restaurant API

The assignment is to implement a back-end which emulates a self service restaurant environment.
## Tasks completed

 - Buillt a REST API using Django REST Framework.
 - Swagger implemented for API documentation
 - Containerized application using Docker.
 - Async API calls using Celery with RabbitMQ as a message broker.
 - API Endpoints for ordering food, collecting food, generating invoice, assigning tables to customers and returning foods.
## Built With

- [Django REST Framework](https://www.django-rest-framework.org)

- [RabbitMQ](https://www.rabbitmq.com)

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)

- [docker-compose](https://docs.docker.com/compose/install/)

## Installation and Usage

1. Clone this repository and change directory.

```bash
git clone https://github.com/Rugz007/ResturantAPI.git
cd ResturantAPI
```
2. Run the following command to **build** all the containers
```bash
docker-compose build
```
4. Run the following command to **run** all the containers

```bash
docker-compose up
```

5. Visit django-admin at ```localhost:8000/admin/``` for admin panel
## Note
- Admin user with username as *admin* and password as *admin* is created.
- Used black as python formatter.

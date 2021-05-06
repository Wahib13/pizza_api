# README #

### What is this repository for? ###

* This is a pizza application API. CRUD operations for pizzas and customers.

### How do I get set up? ###

* Install docker-compose (tested with Docker version 20.10.5, docker-compose version 1.29.0)
* Enter the root of the project directory
* Make a copy of _.env.example_ and name it _.env_. Feel free to edit the default values if you wish
* Bring up the application with docker-compose
```
docker-compose up
```
* Visit http://localhost:8000/api/ in your browser

### How do I manually test the API? ###

* Start by creating a customer. A pizza order cannot be created without a customer

```
POST http://localhost:8000/api/customers/
    {
        "name": "John Doe",
        "phone_number": "2331",
        "address": "1st Street"
    }
```

* Create an order for this customer

```
POST http://localhost:8000/api/orders/
    {
        "customer": 1,
        "pizza_set": [
            {
                "flavour": "MG",
                "size": "M",
                "count": 8
            },
            {
                "flavour": "MA",
                "size": "M",
                "count": 5
            }
        ]
    }
```

* Update an order's pizza set

```
PATCH http://localhost:8000/api/orders/1/
    {
        "pizza_set": [
            {
                "flavour": "MG",
                "size": "S",
                "count": 4
            },
            {
                "flavour": "MA",
                "size": "M",
                "count": 1
            }
        ]
    }
```

* Update an order's status

```
PATCH http://localhost:8000/api/orders/1/
    {
        "status": "DE"
    }
```

* Delete an order

```
DELETE http://localhost:8000/api/orders/1/
```


* All the above can be run from the browsable API or your preferred requesting client

### How do I run automated tests? ###

####1. Via docker-compose
* Ensure the containers are not currently running
```
docker-compose -f docker-compose.yml -f docker-compose.test.yml up
```
* **Ctrl+C** to bring down the other containers after the tests have finished running

####2. Within the container while app is running

```
docker exec -it [web_app_container_name] /bin/bash/
``` 

in my case, **web_app_container_name** is **pizzaapi_web_1**

* When presented with the bash prompt in the container, 
```
    python manage.py test
```

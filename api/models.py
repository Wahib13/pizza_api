from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)
    address = models.TextField()


class Order(models.Model):
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True, blank=True)
    RECEIVED = 'RE'
    DISPATCHED = 'DI'
    DELIVERED = 'DE'
    STATUS_CHOICES = [
        (RECEIVED, 'RECEIVED'),
        (DISPATCHED, 'DISPATCHED'),
        (DELIVERED, 'DELIVERED'),
    ]
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, default=RECEIVED)


class Pizza(models.Model):
    MARGARITA = 'MG'
    MARINARA = 'MA'
    SALAMI = 'SA'
    FLAVOUR_CHOICES = [
        (MARGARITA, 'margarita'),
        (MARINARA, 'marinara'),
        (SALAMI, 'salami'),
    ]
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    SIZE_CHOICES = [
        (SMALL, 'SMALL'),
        (MEDIUM, 'MEDIUM'),
        (LARGE, 'LARGE'),
    ]
    flavour = models.CharField(choices=FLAVOUR_CHOICES, max_length=2)
    size = models.CharField(choices=SIZE_CHOICES, max_length=2)

    order = models.ForeignKey(Order, models.CASCADE)

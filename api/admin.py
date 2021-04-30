from django.contrib import admin

# Register your models here.
from api.models import *
admin.site.register(Pizza)
admin.site.register(Customer)
admin.site.register(Order)

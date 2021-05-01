from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from api.models import Order
from api.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save()

from rest_framework import serializers

from api.models import Order, Pizza


class PizzaSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(default=1)

    class Meta:
        model = Pizza
        fields = ('id', 'flavour', 'size', 'count')

    def create(self, validated_data):
        return Pizza.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    pizza_set = PizzaSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'status', 'pizza_set')

    def create(self, validated_data):
        pizza_set = validated_data.pop('pizza_set')

        order = Order.objects.create(**validated_data)

        for pizza in pizza_set:
            # print(f'pizza: {type(pizza)}')
            pizza['order'] = order
            Pizza.objects.create(**pizza)
        return order

    def validate_pizza_set(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError('order requires at least one pizza')
        return value

    # def update(self, instance, validated_data):
    #     return

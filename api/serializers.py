import logging
from collections import Counter, OrderedDict

from rest_framework import serializers

from api.models import Order, Pizza

logger = logging.getLogger(__name__)


class PizzaSetSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        print('wahib')
        pizzas = []
        for pizza_validated_data in validated_data:
            count = pizza_validated_data.pop('count')
            for i in range(count):
                pizzas.append(Pizza.objects.create(**pizza_validated_data))
        return pizzas

    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
        pizzas = data.all()

        pizza_groups = [
            self.child.to_representation(pizza) for pizza in pizzas
        ]

        # convert the list of ordered dicts to a list of tuples so they can be counted
        pizza_tuples = ordered_dict_list_to_tuple_list(pizza_groups)
        # count them
        tuples_counted = Counter(pizza_tuples).items()
        # convert back to list of ordered dicts
        aggregated_pizza_groups = counted_items_to_ordered_dict_list(tuples_counted)

        return aggregated_pizza_groups


class PizzaSerializer(serializers.ModelSerializer):
    """
    separate the serializer of the sets of pizzas in each order
    """
    count = serializers.IntegerField(default=1)
    order_id = serializers.IntegerField(required=False, write_only=True, source='order.id')

    class Meta:
        model = Pizza
        list_serializer_class = PizzaSetSerializer
        fields = ('flavour', 'size', 'count', 'order_id')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance, count=None):
        ret_value = super(PizzaSerializer, self).to_representation(instance)
        if count:
            ret_value['count'] = count
        return ret_value


class PizzaSet:
    def __init__(self, flavour, size, count, ):
        try:
            pass
        except KeyError:
            logger.exception('invalid count')


class OrderSerializer(serializers.ModelSerializer):
    # a group of the same pizza
    pizza_set = PizzaSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'status', 'pizza_set')

    def create(self, validated_data):
        pizza_set = validated_data.pop('pizza_set')

        order = Order.objects.create(**validated_data)

        # this will call PizzaSetSerializer (many=True)
        pizza_set_serializer = PizzaSerializer(data=pizza_set, many=True)
        if pizza_set_serializer.is_valid():
            pizza_set_serializer.save(order_id=order.id)
        return order

    def validate_pizza_set(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError('order requires at least one pizza')
        return value

    def update(self, instance, validated_data):
        instance.save()
        return instance


def ordered_dict_list_to_tuple_list(ordered_dict_list):
    tuple_list = []
    for ordered in ordered_dict_list:
        tuple_list.append(tuple(zip(ordered.keys(), ordered.values())))
    return tuple_list


def counted_items_to_ordered_dict_list(counted_items):
    res = []
    for item, count in counted_items:
        o = OrderedDict(list(item))
        o['count'] = count
        res.append(o)
    return res

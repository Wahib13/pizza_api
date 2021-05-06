import urllib

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Customer, Order, Pizza


class OrderTestCase(APITestCase):
    def setUp(self) -> None:
        self.customer = Customer.objects.create(name='John Doe',
                                                phone_number='23301',
                                                address='Accra')
        self.customer2 = Customer.objects.create(name='Jane Doe',
                                                 phone_number='24501',
                                                 address='Nigeria')

    def test_orders(self):
        # create an order and get all orders
        url = '/api/orders/'
        order_json = {
            "customer": self.customer.id,
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
        order_json2 = {
            "customer": self.customer2.id,
            "status": 'DI',
            "pizza_set": [
                {
                    "flavour": "MG",
                    "size": "M",
                    "count": 7
                },
                {
                    "flavour": "MA",
                    "size": "L",
                    "count": 1
                }
            ]
        }
        response = self.client.post(url, order_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order_id = response.json().get('id')
        self.assertEqual(Order.objects.get(id=order_id).pizza_set.count(), 13)

        # get all orders
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)

        # filter orders based on status
        response = self.client.get(url, {"status": "DI"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for order_filtered in response.json():
            self.assertEqual(order_filtered.get('pizza_set'), order_json2.get('pizza_set'))

        # filter orders based on customer
        response = self.client.get(url, {"customer": self.customer2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for order_filtered in response.json():
            self.assertEqual(order_filtered.get('customer'), order_json2.get('customer'))

    def test_single_order(self):
        # get one order, update, delete
        url_create = '/api/orders/'
        url_get = '/api/orders/'
        pizza_set = [
            {
                "flavour": "MG",
                "size": "M",
                "count": 2
            },
            {
                "flavour": "MA",
                "size": "M",
                "count": 1
            }
        ]
        order_json = {
            "customer": self.customer.id,
            "pizza_set": pizza_set
        }
        response = self.client.post(url_create, order_json, format='json')

        response_get = self.client.get(f'{url_get}{str(response.json().get("id"))}/', format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.json().get('pizza_set'), pizza_set)
        self.assertEqual(response_get.json().get('customer'), self.customer.id)
        # make sure customer info is included
        self.assertIsNotNone(response_get.json().get('customer_info'))

        pizza_set_update = [
            {
                "flavour": "MG",
                "size": "S",
                "count": 8
            },
            {
                "flavour": "SA",
                "size": "L",
                "count": 2
            }
        ]
        update_order_json = {
            "status": "DE",
            "pizza_set": pizza_set_update
        }
        # update a pizza
        response_patch = self.client.patch(f'{url_get}{str(response.json().get("id"))}/', update_order_json, format='json')

        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(response_patch.json().get('pizza_set'), pizza_set_update)
        self.assertEqual(response_patch.json().get('status'), update_order_json.get('status'))

        order_id = response_patch.json().get('id')
        self.assertEqual(Order.objects.get(id=order_id).pizza_set.count(), 10)

        # updating a delivered order should fail
        response_failed_patch = self.client.patch(f'{url_get}{str(response.json().get("id"))}/', update_order_json, format='json')
        self.assertEqual(response_failed_patch.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

        # delete a pizza
        response_delete = self.client.delete(f'{url_get}{str(response.json().get("id"))}/')
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

        # make sure its gone
        response_get = self.client.get(f'{url_get}{str(response.json().get("id"))}/', format='json')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)


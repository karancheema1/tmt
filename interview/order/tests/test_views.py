from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from interview.order.models import Order
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage
from datetime import date


class OrderListByDateRangeViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.inventory_type = InventoryType.objects.create(name="Test Type")
        self.inventory_language = InventoryLanguage.objects.create(name="Test Language")
        self.inventory = Inventory.objects.create(
            name="Test Inventory",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={}
        )

        self.order1 = Order.objects.create(
            inventory=self.inventory,
            start_date=date(2023, 1, 1),
            embargo_date=date(2023, 3, 31)
        )
        self.order2 = Order.objects.create(
            inventory=self.inventory,
            start_date=date(2023, 2, 1),
            embargo_date=date(2023, 4, 30)
        )
        self.order3 = Order.objects.create(
            inventory=self.inventory,
            start_date=date(2023, 5, 1),
            embargo_date=date(2023, 7, 31)
        )

        self.url = reverse('order-by-date-range')

    def test_list_orders_by_date_range(self):
        response = self.client.get(f"{self.url}?start_date=2023-02-15&embargo_date=2023-05-15")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_orders_missing_params(self):
        response = self.client.get(f"{self.url}?start_date=2023-02-15")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders_no_results(self):
        response = self.client.get(f"{self.url}?start_date=2023-08-01&embargo_date=2023-09-30")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

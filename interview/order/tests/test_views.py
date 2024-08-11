from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from interview.order.models import Order
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage

class DeactivateOrderViewTests(TestCase):
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
        self.order = Order.objects.create(
            inventory=self.inventory,
            start_date="2023-01-01",
            embargo_date="2023-12-31"
        )
        self.url = reverse('deactivate-order', args=[self.order.id])

    def test_deactivate_order(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)

    def test_deactivate_nonexistent_order(self):
        url = reverse('deactivate-order', args=[123456])  # Random order
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
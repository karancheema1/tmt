from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from interview.inventory.models import Inventory, InventoryType, InventoryLanguage

class InventoryListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('inventory-list')

        self.type = InventoryType.objects.create(name="Test Type")
        self.language = InventoryLanguage.objects.create(name="Test Language")

        now = timezone.now()

        self.item_1 = Inventory.objects.create(
            name="Item 1",
            type=self.type,
            language=self.language,
            metadata={}
        )
        self.item_2 = Inventory.objects.create(
            name="Item 2",
            type=self.type,
            language=self.language,
            metadata={}
        )

        # Override the created_at dates as auto_now_add is set to True
        self.item_1.created_at = now - timedelta(days=10)
        self.item_1.save()
        self.item_2.created_at = now - timedelta(days=2)
        self.item_2.save()

    def test_get_all_inventory(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_inventory_with_date_filter(self):
        filter_date = (timezone.now() - timedelta(days=5)).date()
        response = self.client.get(f"{self.url}?created_after={filter_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Item 2")

    def test_get_inventory_with_future_date(self):
        future_date = (timezone.now() + timedelta(days=1)).date()
        response = self.client.get(f"{self.url}?created_after={future_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_inventory_with_invalid_date_format(self):
        response = self.client.get(f"{self.url}?created_after=invalid-date")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('Invalid date format', response.data['error'])

    def test_get_inventory_with_empty_date(self):
        response = self.client.get(f"{self.url}?created_after=")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return all items

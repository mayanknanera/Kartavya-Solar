from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Cart, CartItem, Product


class CartFlowTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            email="cart@example.com",
            password="pass1234",
            first_name="Cart",
            last_name="User",
        )
        self.client.login(email="cart@example.com", password="pass1234")

        self.product = Product.objects.create(
            name="Test Panel",
            slug="test-panel",
            price=Decimal("100.00"),
            is_active=True,
            stock_quantity=10,
            min_order_quantity=1,
        )

    def test_add_to_cart_invalid_quantity_falls_back_to_default(self):
        response = self.client.post(
            reverse("add_to_cart", args=[self.product.id]),
            {"quantity": "not-a-number"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        cart_item = CartItem.objects.get(cart__user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_remove_item_ajax_returns_cart_totals_and_count(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        response = self.client.post(
            reverse("remove_cart_item", args=[item.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertEqual(payload["cart_count"], 0)
        self.assertEqual(payload["cart_total"], 0.0)
        self.assertTrue(payload["cart_empty"])

    def test_clear_cart_removes_all_items(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        response = self.client.post(reverse("clear_cart"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(cart.items.exists())

# Create your tests here.

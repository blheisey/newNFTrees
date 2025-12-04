from django.test import TestCase
from django.urls import reverse
from accounts.models import Customer, User
from .models import Product, Cart, CartItem


# ----------------------------------------------------
# Model tests
# ----------------------------------------------------
class ProductModelTest(TestCase):
    def test_str_and_fields(self):
        p = Product.objects.create(
            name="Pine Tree",
            description="A nice pine tree",
            category="tree",
            price=49.99,
            inventory=10
        )
        self.assertEqual(str(p), "Pine Tree")
        self.assertEqual(p.category, "tree")
        self.assertEqual(p.price, 49.99)
        self.assertEqual(p.inventory, 10)


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cust", password="pass123", is_customer=True)
        self.customer = Customer.objects.create(user=self.user, phone_number="555-1111")

    def test_cart_creation(self):
        cart = Cart.objects.create(customer=self.customer)
        self.assertEqual(cart.customer, self.customer)


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cust", password="pass123", is_customer=True)
        self.customer = Customer.objects.create(user=self.user, phone_number="555-1111")
        self.product = Product.objects.create(
            name="Ornament",
            category="ornament",
            price=5.99,
            inventory=50
        )
        self.cart = Cart.objects.create(customer=self.customer)

    def test_cart_item_creation(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)
        self.assertEqual(item.cart, self.cart)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 3)


# ----------------------------------------------------
# View tests
# ----------------------------------------------------
class ProductViewsTest(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name="Tree1", category="tree", price=10, inventory=5)
        self.product2 = Product.objects.create(name="NFT1", category="nft", price=100, inventory=1)

    def test_product_list_view_all(self):
        url = reverse("shop:product_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_product_list_view_filter_category(self):
        url = reverse("shop:product_list") + "?category=tree"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_product_detail_view(self):
        url = reverse("shop:product_detail", args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)


class CartViewsTest(TestCase):
    def setUp(self):
        # create user and login
        self.user = User.objects.create_user(username="cust", password="pass123", is_customer=True)
        self.customer = Customer.objects.create(user=self.user, phone_number="555-1111")
        self.client.login(username="cust", password="pass123")

        # create products
        self.product1 = Product.objects.create(name="Tree1", category="tree", price=10, inventory=5)
        self.product2 = Product.objects.create(name="NFT1", category="nft", price=100, inventory=1)

    def test_add_to_cart_creates_cart_and_item(self):
        url = reverse("shop:add_to_cart", args=[self.product1.id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


        cart = Cart.objects.get(customer=self.customer)
        item = CartItem.objects.get(cart=cart, product=self.product1)
        self.assertEqual(item.quantity, 1)

        # adding same product again increments quantity
        response = self.client.post(url, follow=True)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)

    def test_remove_from_cart(self):
        cart = Cart.objects.create(customer=self.customer)
        item = CartItem.objects.create(cart=cart, product=self.product1, quantity=1)

        url = reverse("shop:remove_from_cart", args=[self.product1.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CartItem.objects.filter(cart=cart, product=self.product1).exists())

    def test_update_cart_item_quantity(self):
        cart = Cart.objects.create(customer=self.customer)
        item = CartItem.objects.create(cart=cart, product=self.product1, quantity=1)

        url = reverse("shop:update_cart_item", args=[self.product1.id])
        response = self.client.post(url, {"quantity": 5}, follow=True)
        self.assertEqual(response.status_code, 200)

        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)

        # setting quantity to 0 removes item
        response = self.client.post(url, {"quantity": 0}, follow=True)
        self.assertFalse(CartItem.objects.filter(cart=cart, product=self.product1).exists())

    def test_cart_view_shows_items(self):
        cart = Cart.objects.create(customer=self.customer)
        item1 = CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        item2 = CartItem.objects.create(cart=cart, product=self.product2, quantity=1)

        url = reverse("shop:cart")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)



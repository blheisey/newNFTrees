from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Customer, DriverProfile

User = get_user_model()


# ----------------------------------------------------
# Model tests
# ----------------------------------------------------
class UserModelTest(TestCase):
    def test_str(self):
        user = User.objects.create(username="alice", is_customer=True)
        self.assertEqual(str(user), "alice")

    def test_user_flags(self):
        user = User.objects.create(username="bob", is_driver=True)
        self.assertTrue(user.is_driver)
        self.assertFalse(user.is_customer)


class CustomerModelTest(TestCase):
    def test_customer_str(self):
        user = User.objects.create(username="charlie")
        customer = Customer.objects.create(user=user, phone_number="555-1111")

        self.assertEqual(str(customer), "charlie")
        self.assertEqual(customer.phone_number, "555-1111")
        self.assertEqual(customer.user.username, "charlie")


class DriverProfileModelTest(TestCase):
    def test_driver_profile_str(self):
        user = User.objects.create(username="dave", is_driver=True)
        profile = DriverProfile.objects.create(user=user, location="Warehouse")

        self.assertEqual(str(profile), "dave")
        self.assertEqual(profile.location, "Warehouse")

    def test_employee_id_is_auto_generated(self):
        user = User.objects.create(username="eve", is_driver=True)
        profile = DriverProfile.objects.create(user=user)

        self.assertIsNotNone(profile.employee_id)


# ----------------------------------------------------
# View tests
# ----------------------------------------------------
class EmployeeSignUpViewTest(TestCase):
    def test_get_signup_page(self):
        url = reverse("employee_signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/employee_signup.html")

    def test_valid_employee_signup(self):
        url = reverse("employee_signup")
        response = self.client.post(url, {
            "username": "driver1",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        })
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

        # User should exist
        self.assertTrue(User.objects.filter(username="driver1").exists())


class CustomerSignupViewTest(TestCase):
    def test_get_signup_page(self):
        url = reverse("signup")  # updated
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_valid_customer_signup(self):
        url = reverse("signup")  # updated
        response = self.client.post(url, {
            "username": "customer1",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))
        self.assertTrue(User.objects.filter(username="customer1").exists())


class EditCustomerProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="pass123"
        )
        self.url = reverse("customer_change")  # updated

    def test_get_profile_edit_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_post_profile_edit(self):
        self.client.login(username="testuser", password="pass123")
        response = self.client.post(self.url, {
            "username": "updateduser"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("shop:product_list"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")


class EditDriverProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="driver", password="pass123", is_driver=True
        )
        self.profile = DriverProfile.objects.create(user=self.user)
        self.url = reverse("driver_change")

    def test_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_can_update_driver(self):
        self.client.login(username="driver", password="pass123")

        response = self.client.post(self.url, {
            "username": "driver_updated"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("shop:product_list"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "driver_updated")


class EmployeePortalViewTest(TestCase):
    def test_employee_portal_renders(self):
        url = reverse("employee_portal")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employee_portal.html")

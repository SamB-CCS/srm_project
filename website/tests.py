from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import (
    SignupForm,
    AddCustomerForm,
    AddSupplierForm,
    AddDetailForm,
    AddExclusionForm,
)


class SignupFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_email_already_registered(self):
        User.objects.create(email="existing@example.com")
        form_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "existing@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This email address is already registered.", form.errors["email"])


class AddCustomerFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "+1 123-456-7890",
            "address": "123 Main St",
            "city": "Anytown",
            "country": "USA",
            "postcode": "ABC 123",
        }
        form = AddCustomerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_fields(self):
        form_data = {
            "first_name": "John123",  # First name should only contain letters
            "last_name": "Doe123",  # Last name should only contain letters
            "email": "invalid_email",  # Invalid email format
            "phone": "123",  # Invalid phone number format
            "address": "Invalid@Address",  # Address should only contain alphanumeric and spaces
            "city": "Anytown123",  # City should only contain letters
            "country": "USA123",  # Country should only contain letters
            "postcode": "invalid_postcode",  # Invalid postcode format
        }
        form = AddCustomerForm(data=form_data)
        self.assertFalse(form.is_valid())


class AddSupplierFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            "supplier_name": "John",
            "supplier_email": "john@example.com",
            "supplier_phone": "+1 123-456-7890",
            "supplier_address": "123 Main St",
            "supplier_city": "Anytown",
            "supplier_country": "USA",
            "supplier_postcode": "ABC 123",
        }
        form = AddSupplierForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_fields(self):
        form_data = {
            "supplier_name": "John123$",  # First name should only contain letters & numbers
            "supplier_email": "invalid_email",  # Invalid email format
            "supplier_phone": "123",  # Invalid phone number format
            "supplier_address": "Invalid@Address",  # Address should only contain alphanumeric and spaces
            "supplier_city": "Anytown123",  # City should only contain letters
            "supplier_country": "USA123",  # Country should only contain letters
            "supplier_postcode": "invalid_postcode",  # Invalid postcode format
        }
        form = AddSupplierForm(data=form_data)
        self.assertFalse(form.is_valid())


class AddDetailFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            "company_type": "Agricultural",
            "legal_form": "Charity",
            "vat_no": "GB123456789",
        }
        form = AddDetailForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_fields(self):
        form_data = {
            "company_type": "Computers",  # company type should only contain certain values
            "legal_form": "test",  # Legal form should only contain certain values
            "vat_no": "invalid",  # Invalid vat number format
        }
        form = AddDetailForm(data=form_data)
        self.assertFalse(form.is_valid())


class AddExclusionFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            "mandatory": "Theft",
            "discretionary": "Bankruptcy",
            "exclusion_date": "27/03/23",
        }
        form = AddExclusionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_fields(self):
        form_data = {
            "mandatory": "John123",  # Mandatory should only contain certain values
            "discretionary": "Doe123",  # Discretionary should only contain certain values
            "exclusion_date": "98782",  # Invalid date format
        }
        form = AddExclusionForm(data=form_data)
        self.assertFalse(form.is_valid())


class AddCustomerViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_add_customer_view_with_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("add_customer"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_customer.html")

    def test_add_customer_view_with_unauthenticated_user(self):
        response = self.client.get(reverse("add_customer"))
        self.assertEqual(response.status_code, 302)

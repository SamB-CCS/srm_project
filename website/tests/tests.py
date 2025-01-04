import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from website.forms import (
    SignupForm,
    AddCustomerForm,
    AddSupplierForm,
    AddDetailForm,
    AddExclusionForm,
)


@pytest.mark.django_db
class TestSignupForm:
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
        assert form.is_valid()

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
        assert not form.is_valid()
        assert "This email address is already registered." in form.errors["email"]


@pytest.mark.django_db
class TestAddCustomerForm:
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
        assert form.is_valid()

    def test_invalid_form_fields(self):
        form_data = {
            "first_name": "John123",
            "last_name": "Doe123",
            "email": "invalid_email",
            "phone": "123",
            "address": "Invalid@Address",
            "city": "Anytown123",
            "country": "USA123",
            "postcode": "invalid_postcode",
        }
        form = AddCustomerForm(data=form_data)
        assert not form.is_valid()


@pytest.mark.django_db
class TestAddSupplierForm:
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
        assert form.is_valid()

    def test_invalid_form_fields(self):
        form_data = {
            "supplier_name": "John123$",
            "supplier_email": "invalid_email",
            "supplier_phone": "123",
            "supplier_address": "Invalid@Address",
            "supplier_city": "Anytown123",
            "supplier_country": "USA123",
            "supplier_postcode": "invalid_postcode",
        }
        form = AddSupplierForm(data=form_data)
        assert not form.is_valid()


@pytest.mark.django_db
class TestAddDetailForm:
    def test_valid_form(self):
        form_data = {
            "company_type": "Agricultural",
            "legal_form": "Charity",
            "vat_no": "GB123456789",
        }
        form = AddDetailForm(data=form_data)
        assert form.is_valid()

    def test_invalid_form_fields(self):
        form_data = {
            "company_type": "Computers",
            "legal_form": "test",
            "vat_no": "invalid",
        }
        form = AddDetailForm(data=form_data)
        assert not form.is_valid()

@pytest.mark.django_db
class TestAddExclusionForm:
    def test_valid_form(self):
        form_data = {
            "mandatory": "Theft",
            "discretionary": "Bankruptcy",
            "exclusion_date": "27/03/23",
        }
        form = AddExclusionForm(data=form_data)
        assert form.is_valid()

    def test_invalid_form_fields(self):
        form_data = {
            "mandatory": "John123",
            "discretionary": "Doe123",
            "exclusion_date": "98782",
        }
        form = AddExclusionForm(data=form_data)
        assert not form.is_valid()

@pytest.mark.django_db
class TestAddCustomerView:
    @pytest.fixture
    def authenticated_client(self):
        client = Client()
        user = User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        return client

    def test_add_customer_view_with_authenticated_user(self, authenticated_client):
        response = authenticated_client.get(reverse("add_customer"))
        assert response.status_code == 200
        assert "add_customer.html" in [t.name for t in response.templates]

    def test_add_customer_view_with_unauthenticated_user(self, client):
        response = client.get(reverse("add_customer"))
        assert response.status_code == 302

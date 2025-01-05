import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from pytest_django.asserts import assertTemplateUsed
from django.urls import reverse
from website.models import Customer, Supplier, Detail, Exclusion
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

    def test_register_user_with_different_passwords(self, client):
        form_data = {
            "username": "newuser",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password1": "newpassword123",
            "password2": "differentpassword",
            }
        form = SignupForm(data=form_data)
        assert not form.is_valid()
        assert "The passwords do not match."

    def test_register_user_with_similar_password_to_inputs(self, client):
        form_data = {
            "username": "newuser",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password1": "jane@example.com",
            "password2": "jane@example.com",
            }
        form = SignupForm(data=form_data)
        assert not form.is_valid()
        assert "The password is too similar to other fields."

    def test_register_user_with_number_password(self, client):
        form_data = {
            "username": "newuser",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password1": "123456789",
            "password2": "123456789",
            }
        form = SignupForm(data=form_data)
        assert not form.is_valid()
        assert "The password can not be entirely numbers."

    def test_register_user_with_low_character_password(self, client):
        form_data = {
            "username": "newuser",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password1": "ptyu123",
            "password2": "ptyu123",
            }
        form = SignupForm(data=form_data)
        assert not form.is_valid()
        assert "The password can not be entirely numbers."

    def test_register_user_with_common_password(self, client):
        form_data = {
            "username": "newuser",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password1": "password123",
            "password2": "password123",
            }
        form = SignupForm(data=form_data)
        assert not form.is_valid()
        assert "The password is too common."


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
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        return client

    def test_add_customer_view_with_authenticated_user(self, authenticated_client):
        response = authenticated_client.get(reverse("add_customer"))
        assert response.status_code == 200
        assert "add_customer.html" in [t.name for t in response.templates]

    def test_add_customer_view_with_unauthenticated_user(self, client):
        response = client.get(reverse("add_customer"))
        assert response.status_code == 302


@pytest.mark.django_db
class TestHomeView:
    @pytest.fixture
    def authenticated_client(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        return client

    def test_home_view_with_authenticated_user(self, authenticated_client):
        response = authenticated_client.get(reverse("home"))
        assert response.status_code == 200
        assert "customers" in response.context

    def test_home_view_with_unauthenticated_user(self, client):
        response = client.get(reverse("home"))
        assert response.status_code == 200  # Should still allow access to the home page

    def test_login_success(self, client):
        User.objects.create_user(username="testuser", password="testpassword")
        response = client.post(reverse("home"), {
            "username": "testuser",
            "password": "testpassword"
        })
        assert response.status_code == 302  # Redirect after successful login
        assert response.wsgi_request.user.is_authenticated

    def test_login_failure(self, client):
        response = client.post(reverse("home"), {
            "username": "wronguser",
            "password": "wrongpassword"
        })
        assert response.status_code == 302  # Redirect after failed login
        assert not response.wsgi_request.user.is_authenticated

    def test_login_blocked_after_max_attempts(self, client):
        User.objects.create_user(username="testuser", password="testpassword")
        for _ in range(10):  # Exceed max attempts
            client.post(reverse("home"), {
                "username": "testuser",
                "password": "wrongpassword"
            })
        response = client.post(reverse("home"), {
            "username": "testuser",
            "password": "testpassword"
        })
        # Check for a 302 redirect
        assert response.status_code == 302  # Should be redirected
        # Check the redirect location (it should redirect back to the home page)
        assert response.url == reverse("home")  # Ensure it redirects to the home page
        # Check if the message is in the response context
        messages = list(get_messages(response.wsgi_request))
        assert any("Account temporarily locked due to too many failed attempts" in str(message) for message in messages)


@pytest.mark.django_db
class TestUserLogout:
    @pytest.fixture
    def authenticated_client(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        return client

    def test_logout_view(self, authenticated_client):
        response = authenticated_client.post(reverse("user_logout"), {"confirm_logout": "yes"})
        assert response.status_code == 302  # Redirect after logout
        assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
class TestCustomerUpdate:
    @pytest.fixture
    def authenticated_client(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        return client

    @pytest.mark.django_db
    def test_update_customer_with_authenticated_user(self, authenticated_client):
        # Create initial customer with all required fields
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
            city="London",
            country="UK",
            postcode="SW1A 1AA"
        )

        # Updated data
        update_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "phone": "0987654321",
            "address": "456 High St",
            "city": "Manchester",
            "country": "UK",
            "postcode": "M1 1AA"
        }

        response = authenticated_client.post(
            reverse("update_customer", kwargs={"pk": customer.pk}),
            update_data
        )
        assert response.status_code == 302
        assert response.url == reverse("home")

        # Verify updates
        updated_customer = Customer.objects.get(pk=customer.pk)
        assert updated_customer.first_name == "Jane"
        assert updated_customer.last_name == "Smith"


class TestSupplierUpdate:
    @pytest.fixture
    def authenticated_client(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        return client

    @pytest.fixture
    def test_customer(self):
        return Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
            city="London",
            country="UK",
            postcode="SW1A 1AA"
        )

    @pytest.mark.django_db
    def test_update_supplier_with_authenticated_user(self, authenticated_client, test_customer):
        supplier = Supplier.objects.create(
            supplier_name="Test Supplier",
            supplier_email="supplier@test.com",
            supplier_phone="1234567890",
            supplier_address="123 Supplier St",
            supplier_city="London",
            supplier_country="UK",
            supplier_postcode="SW1A 1AA",
            customer_id=test_customer
        )

        update_data = {
            "supplier_name": "Updated Supplier",
            "supplier_email": "updated@test.com",
            "supplier_phone": "0987654321",
            "supplier_address": "456 Supplier St",
            "supplier_city": "Manchester",
            "supplier_country": "UK",
            "supplier_postcode": "M1 1AA"
        }

        response = authenticated_client.post(
            reverse("update_supplier", kwargs={"pk": supplier.pk}),
            update_data
        )
        assert response.status_code == 302
        assert response.url == reverse("home")

        updated_supplier = Supplier.objects.get(pk=supplier.pk)
        assert updated_supplier.supplier_name == "Updated Supplier"


class TestDetailUpdate:
    @pytest.fixture
    def authenticated_client(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        return client

    @pytest.fixture
    def test_setup(self):
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
            city="London",
            country="UK",
            postcode="SW1A 1AA"
        )
        supplier = Supplier.objects.create(
            supplier_name="Test Supplier",
            supplier_email="supplier@test.com",
            supplier_phone="1234567890",
            supplier_address="123 Supplier St",
            supplier_city="London",
            supplier_country="UK",
            supplier_postcode="SW1A 1AA",
            customer_id=customer
        )
        return supplier

    @pytest.mark.django_db
    def test_update_detail_with_authenticated_user(self, authenticated_client, test_setup):
        detail = Detail.objects.create(
            company_type="IT Services",
            legal_form="Limited Company",
            vat_no="GB123456789",
            supplier_id=test_setup
        )

        update_data = {
            "company_type": "Education & Training",
            "legal_form": "Sole Trader",
            "vat_no": "GB987654321"
        }

        response = authenticated_client.post(
            reverse("update_detail", kwargs={"pk": detail.pk}),
            update_data
        )
        assert response.status_code == 302
        assert response.url == reverse("home")

        updated_detail = Detail.objects.get(pk=detail.pk)
        assert updated_detail.company_type == "Education & Training"


class TestExclusionUpdate:
    @pytest.fixture
    def authenticated_client(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        return client

    @pytest.fixture
    def test_setup(self):
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
            city="London",
            country="UK",
            postcode="SW1A 1AA"
        )
        supplier = Supplier.objects.create(
            supplier_name="Test Supplier",
            supplier_email="supplier@test.com",
            supplier_phone="1234567890",
            supplier_address="123 Supplier St",
            supplier_city="London",
            supplier_country="UK",
            supplier_postcode="SW1A 1AA",
            customer_id=customer
        )
        return supplier

    @pytest.mark.django_db
    def test_update_exclusion_with_authenticated_user(self, authenticated_client, test_setup):
        exclusion = Exclusion.objects.create(
            mandatory="None",
            discretionary="None",
            supplier_id=test_setup
        )

        update_data = {
            "mandatory": "Fraud",
            "discretionary": "Bankruptcy",
            "exclusion_date": "2025-01-05"
        }

        response = authenticated_client.post(
            reverse("update_exclusion", kwargs={"pk": exclusion.pk}),
            update_data
        )
        assert response.status_code == 302
        assert response.url == reverse("home")

        updated_exclusion = Exclusion.objects.get(pk=exclusion.pk)
        assert updated_exclusion.mandatory == "Fraud"
        assert updated_exclusion.discretionary == "Bankruptcy"

    @pytest.mark.django_db
    def test_update_exclusion_with_invalid_form(self, authenticated_client, test_setup):
        # Create initial exclusion
        exclusion = Exclusion.objects.create(
            mandatory="None",
            discretionary="None",
            supplier_id=test_setup
        )

        # Submit form with invalid choice data
        update_data = {
            'mandatory': 'InvalidChoice',  # Not in choices
            'discretionary': 'InvalidChoice',  # Not in choices
        }

        response = authenticated_client.post(
            reverse("update_exclusion", kwargs={"pk": exclusion.pk}),
            update_data
        )

        # View should re-render the form
        assert response.status_code == 200

        # Check if the response contains the expected form
        assert "form" in response.context

        # Check if the correct template is used
        assert "update_exclusion.html" in [template.name for template in response.templates]

        # Form should contain errors
        form = response.context['form']
        assert form.errors

        # Database should not be updated
        exclusion.refresh_from_db()
        assert exclusion.mandatory == "None"
        assert exclusion.discretionary == "None"


class TestCustomerRecord:
    @pytest.fixture
    def authenticated_client(self):
        client = Client()
        User.objects.create_user(username="testuser", password="testpassword")
        client.login(username="testuser", password="testpassword")
        return client

    @pytest.fixture
    def test_data(self):
        # Create customer
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
            city="London",
            country="UK",
            postcode="SW1A 1AA"
        )

        # Create multiple suppliers for this customer
        suppliers = []
        for i in range(2):
            supplier = Supplier.objects.create(
                supplier_name=f"Test Supplier {i}",
                supplier_email=f"supplier{i}@test.com",
                supplier_phone="1234567890",
                supplier_address=f"{i} Supplier St",
                supplier_city="London",
                supplier_country="UK",
                supplier_postcode="SW1A 1AA",
                customer_id=customer
            )
            suppliers.append(supplier)

            # Create detail for each supplier
            Detail.objects.create(
                company_type="IT Services",
                legal_form="Limited Company",
                vat_no=f"GB12345678{i}",
                supplier_id=supplier
            )

            # Create exclusion for each supplier
            Exclusion.objects.create(
                mandatory="None",
                discretionary="None",
                supplier_id=supplier
            )

        return customer, suppliers

    @pytest.mark.django_db
    def test_customer_record_with_authenticated_user(self, authenticated_client, test_data):
        customer, suppliers = test_data

        response = authenticated_client.get(
            reverse("customer", kwargs={"pk": customer.pk})
        )

        # Check basic response
        assert response.status_code == 200
        assertTemplateUsed(response, "customer.html")

        # Check context data
        assert response.context["customer_record"] == customer
        assert len(response.context["suppliers"]) == 2
        assert len(response.context["details"]) == 2
        assert len(response.context["exclusions"]) == 2

        # Verify relationships
        for i, supplier in enumerate(response.context["suppliers"]):
            assert supplier.customer_id == customer
            assert response.context["details"][i].supplier_id == supplier
            assert response.context["exclusions"][i].supplier_id == supplier

    @pytest.mark.django_db
    def test_customer_record_with_no_suppliers(self, authenticated_client):
        # Test customer record with no related suppliers
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            phone="1234567890",
            address="123 Main St",
            city="London",
            country="UK",
            postcode="SW1A 1AA"
        )

        response = authenticated_client.get(
            reverse("customer", kwargs={"pk": customer.pk})
        )

        assert response.status_code == 200
        assert len(response.context["suppliers"]) == 0
        assert len(response.context["details"]) == 0
        assert len(response.context["exclusions"]) == 0

    @pytest.mark.django_db
    def test_customer_record_with_unauthenticated_user(self, client, test_data):
        customer, _ = test_data

        response = client.get(
            reverse("customer", kwargs={"pk": customer.pk})
        )

        assert response.status_code == 302
        assert response.url == reverse("home")
        messages = list(get_messages(response.wsgi_request))
        assert str(messages[0]) == "You must be logged in to view details"

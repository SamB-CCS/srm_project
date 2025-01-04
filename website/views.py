from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import (
    SignupForm,
    AddCustomerForm,
    AddSupplierForm,
    AddDetailForm,
    AddExclusionForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from formtools.wizard.views import SessionWizardView
from .models import Customer, Supplier, Detail, Exclusion
import logging
from django.core.cache import cache

logger = logging.getLogger("django")


# Login method
def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_login_attempts(request, username):
    """
    Check if user has exceeded login attempts
    Returns tuple of (is_blocked, attempts_remaining, block_time_remaining)
    """
    MAX_ATTEMPTS = 10
    BLOCK_TIME = 30  # minutes
    # Create a unique key for this IP and username combination
    client_ip = get_client_ip(request)
    cache_key = f"login_attempts_{client_ip}_{username}"
    block_key = f"login_blocked_{client_ip}_{username}"  # Check if user is currently blocked
    is_blocked = cache.get(block_key, False)
    if is_blocked:
        block_time = BLOCK_TIME * 60  # Convert minutes to seconds
        return True, 0, block_time // 60  # Convert seconds to minutes
    # Get current attempts
    attempts = cache.get(cache_key, 0)

    return False, MAX_ATTEMPTS - attempts, 0


def increment_login_attempts(request, username):
    """
    Increment login attempts and block if necessary
    Returns tuple of (is_blocked, attempts_remaining, block_time_remaining)
    """
    MAX_ATTEMPTS = 10
    BLOCK_TIME = 30  # minutes
    client_ip = get_client_ip(request)
    cache_key = f"login_attempts_{client_ip}_{username}"
    block_key = f"login_blocked_{client_ip}_{username}"
    # Increment attempts
    attempts = cache.get(cache_key, 0) + 1
    if attempts >= MAX_ATTEMPTS:
        # Block the user
        cache.set(block_key, True, timeout=BLOCK_TIME * 60)  # Convert minutes to seconds
        # Reset attempts counter
        cache.delete(cache_key)
        return True, 0, BLOCK_TIME
    else:
        # Set or update attempts
        cache.set(cache_key, attempts, timeout=24 * 60 * 60)  # 24 hour expiry
        return False, MAX_ATTEMPTS - attempts, 0


def home(request):
    customers = Customer.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Check if user is blocked
        is_blocked, attempts_remaining, block_time = check_login_attempts(request, username)
        if is_blocked:
            messages.error(
                request,
                f"Account temporarily locked due to too many failed attempts. "
                f"Please try again in {block_time} minutes."
            )
            return redirect("home")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Reset any login attempt counters on successful login
            client_ip = get_client_ip(request)
            cache.delete(f"login_attempts_{client_ip}_{username}")
            messages.success(request, "You are logged in!")
            return redirect("home")
        else:
            # Increment failed attempts and check if user should be blocked
            is_blocked, attempts_remaining, block_time = increment_login_attempts(request, username)
            logger.error(f"Failed login attempt with username: {username}")
            if is_blocked:
                messages.error(
                    request,
                    f"Account temporarily locked due to too many failed attempts. "
                    f"Please try again in {block_time} minutes."
                )
            else:
                messages.error(
                    request,
                    f"Incorrect email or password. {attempts_remaining} attempts remaining "
                    f"before temporary lockout."
                )
            return redirect("home")
    return render(request, "home.html", {"customers": customers})


# Logout method and logout confirmation
def user_logout(request):
    if request.method == "POST":
        if "confirm_logout" in request.POST:
            logout(request)
            messages.success(request, "You have been logged out...")
            return redirect("home")
    return render(request, "logout_confirm.html")


# Register method
def register_user(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate & Login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered your details!")
            return redirect("home")
    else:
        form = SignupForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})


# Displays all related customer details
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Customer.objects.get(id=pk)
        suppliers = Supplier.objects.filter(customer_id=customer_record)
        details = []
        exclusions = []
        for supplier in suppliers:
            detail = Detail.objects.filter(supplier_id=supplier).first()
            exclusion = Exclusion.objects.filter(supplier_id=supplier).first()
            details.append(detail)
            exclusions.append(exclusion)
        return render(
            request,
            "customer.html",
            {
                "customer_record": customer_record,
                "suppliers": suppliers,
                "details": details,
                "exclusions": exclusions,
            },
        )
    else:
        logger.error(f"User not logged in to view customer record {pk}")
        messages.success(request, "You must be logged in to view details")
        return redirect("home")


# Allows user to amend/update existing customer data fields
def update_customer(request, pk):
    if request.user.is_authenticated:
        update_cust = Customer.objects.get(id=pk)
        form = AddCustomerForm(request.POST or None, instance=update_cust)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer has been updated!")
            return redirect("home")
        return render(request, "update_customer.html", {"form": form})
    else:
        logger.error(f"User not logged in to view update customer {pk}")
        messages.success(request, "You must be logged In to view details")
        return redirect("home")


# Allows user to amend/update existing supplier data fields
def update_supplier(request, pk):
    if request.user.is_authenticated:
        update_supp = Supplier.objects.get(id=pk)
        form = AddSupplierForm(request.POST or None, instance=update_supp)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier has been updated!")
            session_keys_to_remove = ["customer", "supplier"]
            session = request.session
            for key in session_keys_to_remove:
                if key in session:
                    del session[key]
            session.modified = True
            return redirect("home")
        return render(request, "update_supplier.html", {"form": form})
    else:
        logger.error(f"User not logged in to view update supplier {pk}")
        messages.success(request, "You must be logged In to view details")
        return redirect("home")


# Allows user to amend/update existing detail data fields
def update_detail(request, pk):
    if request.user.is_authenticated:
        update_det = Detail.objects.get(id=pk)
        form = AddDetailForm(request.POST or None, instance=update_det)
        if form.is_valid():
            form.save()
            messages.success(request, "Details have been updated!")
            return redirect("home")
        return render(request, "update_detail.html", {"form": form})
    else:
        logger.error(f"User not logged in to view update details {pk}")
        messages.success(request, "You must be logged in to view details")
        return redirect("home")


# Allows user to amend/update existing exclusion data fields
def update_exclusion(request, pk):
    if request.user.is_authenticated:
        update_excl = Exclusion.objects.get(id=pk)
        form = AddExclusionForm(request.POST or None, instance=update_excl)
        if form.is_valid():
            form.save()
            messages.success(request, "Exclusions have been updated!")
            return redirect("home")
        return render(request, "update_exclusion.html", {"form": form})
    else:
        logger.error(f"User not logged in to view update exclusions {pk}")
        messages.success(request, "You must be logged in to view details")
        return redirect("home")


# Form and Template dict and tuple
FORMS = [
    ("customer", AddCustomerForm),
    ("supplier", AddSupplierForm),
    ("detail", AddDetailForm),
    ("exclusion", AddExclusionForm),
]

TEMPLATES = {
    "customer": "add_customer.html",
    "supplier": "add_supplier.html",
    "detail": "add_detail.html",
    "exclusion": "add_exclusion.html",
}


# WizardView class to handle session data between the various forms and pass model instances into relevant forms
class MyWizardView(LoginRequiredMixin, SessionWizardView):
    form_list = FORMS
    templates = TEMPLATES

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        customer_instance = None
        for form in form_list:
            if form.prefix == "customer":
                customer_instance = form.save()
                self.request.session["customer"] = customer_instance
                messages.success(self.request, f"{form.prefix} added...")
            elif form.prefix == "supplier":
                customer = self.request.session.get("customer")
                if customer:
                    form.instance.customer_id = customer
                    customer_instance = form.save()
                    self.request.session["supplier"] = customer_instance
                    messages.success(self.request, f"{form.prefix} added...")
            elif form.prefix == "detail" or "exclusion":
                supplier = self.request.session.get("supplier")
                if supplier:
                    form.instance.supplier_id = supplier
                    customer_instance = form.save()
                    messages.success(self.request, f"{form.prefix} added...")
            else:
                messages.error(self.request, f"{form.prefix} form has errors.")
                return self.render_goto_step(step=self.steps.current)
        # Delete form session keys before returning to the home page
        session_keys_to_remove = ["customer", "supplier"]
        session = self.request.session
        for key in session_keys_to_remove:
            if key in session:
                del session[key]
        session.modified = True
        return redirect("home")

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from .models import Customer, Supplier, Detail, Exclusion
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["username"].label = ""
        self.fields[
            "username"
        ].help_text = '<span class="form-text text-muted"><small>Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = ""
        self.fields[
            "password1"
        ].help_text = "<ul class=\"form-text text-muted small\"><li>Your password can't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can't be a commonly used password.</li><li>Your password can't be entirely numeric.</li></ul>"

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""
        self.fields[
            "password2"
        ].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email


# Form field validators
letter_validator = RegexValidator(
    r"^[a-zA-Z ]+$", "Only letters and spaces are allowed."
)
alphanumeric_validator = RegexValidator(
    r"^[\w\s]+$", "Only alphanumeric characters and spaces are allowed."
)
phone_validator = RegexValidator(
    r"^[+]?(?:[0-9\-\(\)\/\.]\s?){6,15}[0-9]{1}$", "Enter a valid phone number."
)
postcode_validator = RegexValidator(
    r"^[a-zA-Z0-9][a-zA-Z0-9\- ]{0,10}[a-zA-Z0-9]$",
    "Enter a valid postcode/zipcode e.g. N1 1AD.",
)
vat_validator = RegexValidator(
    r"^[Gg][Bb][0-9]{9}([0-9]{3})?$",
    "Enter a valid UK VAT number, GB followed by nine numbers e.g. GB123456789",
)


# Create Add Customer Form
class AddCustomerForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        validators=[letter_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "First Name", "class": "form-control"}
        ),
        label="",
    )
    last_name = forms.CharField(
        required=True,
        validators=[letter_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Last Name", "class": "form-control"}
        ),
        label="",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
        label="",
    )
    phone = forms.CharField(
        required=True,
        validators=[phone_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Phone", "class": "form-control"}
        ),
        label="",
    )
    address = forms.CharField(
        required=True,
        validators=[alphanumeric_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Address", "class": "form-control"}
        ),
        label="",
    )
    city = forms.CharField(
        required=True,
        validators=[letter_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "City", "class": "form-control"}
        ),
        label="",
    )
    country = forms.CharField(
        required=True,
        validators=[letter_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Country", "class": "form-control"}
        ),
        label="",
    )
    postcode = forms.CharField(
        required=True,
        validators=[postcode_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Postcode", "class": "form-control"}
        ),
        label="",
    )

    class Meta:
        model = Customer
        exclude = ("user",)

    # Capitalise strings before saving to databse model
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        return first_name.title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        return last_name.title()

    def clean_address(self):
        address = self.cleaned_data.get("address")
        return address.title()

    def clean_city(self):
        supplier_city = self.cleaned_data.get("city")
        return supplier_city.title()

    def clean_country(self):
        country = self.cleaned_data.get("country")
        return country.title()

    def clean_postcode(self):
        postcode = self.cleaned_data.get("postcode")
        return postcode.upper()


# Create Add Supplier Form
class AddSupplierForm(forms.ModelForm):
    supplier_name = forms.CharField(
        required=True,
        validators=[alphanumeric_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Supplier Name", "class": "form-control"}
        ),
        label="",
    )
    supplier_email = forms.EmailField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Supplier Email", "class": "form-control"}
        ),
        label="",
    )
    supplier_phone = forms.CharField(
        required=True,
        validators=[phone_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Supplier Phone", "class": "form-control"}
        ),
        label="",
    )
    supplier_address = forms.CharField(
        required=True,
        validators=[alphanumeric_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Supplier Address", "class": "form-control"}
        ),
        label="",
    )
    supplier_city = forms.CharField(
        required=True,
        validators=[letter_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Supplier City", "class": "form-control"}
        ),
        label="",
    )
    supplier_country = forms.CharField(
        required=True,
        validators=[letter_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Supplier Country", "class": "form-control"}
        ),
        label="",
    )
    supplier_postcode = forms.CharField(
        required=True,
        validators=[postcode_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Supplier Postcode", "class": "form-control"}
        ),
        label="",
    )

    class Meta:
        model = Supplier
        exclude = (
            "user",
            "customer_id",
        )

    # Capitalise strings before saving to databse model
    def clean_supplier_name(self):
        supplier_name = self.cleaned_data.get("supplier_name")
        return supplier_name.title()

    def clean_supplier_address(self):
        supplier_address = self.cleaned_data.get("supplier_address")
        return supplier_address.title()

    def clean_supplier_city(self):
        supplier_city = self.cleaned_data.get("supplier_city")
        return supplier_city.title()

    def clean_supplier_country(self):
        supplier_country = self.cleaned_data.get("supplier_country")
        return supplier_country.title()

    def clean_supplier_postcode(self):
        supplier_postcode = self.cleaned_data.get("supplier_postcode")
        return supplier_postcode.upper()


# Create Add Details Form
class AddDetailForm(forms.ModelForm):
    company_type = forms.ChoiceField(
        required=True,
        widget=forms.widgets.Select(
            attrs={
                "placeholder": "Company Type e.g. Agricultural etc.",
                "class": "form-control",
            }
        ),
        choices=Detail.COMPANY_TYPE,
        label="",
    )
    legal_form = forms.ChoiceField(
        required=True,
        widget=forms.widgets.Select(
            attrs={
                "placeholder": "Legal Form e.g. Public, Private etc.",
                "class": "form-control",
            }
        ),
        choices=Detail.LEGAL_FORM,
        label="",
    )
    vat_no = forms.CharField(
        required=True,
        validators=[vat_validator],
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "VAT Number", "class": "form-control"}
        ),
        label="",
    )

    class Meta:
        model = Detail
        exclude = (
            "user",
            "supplier_id",
        )

    # Capitalise strings before saving to database model
    def clean_vat_no(self):
        vat_no = self.cleaned_data.get("vat_no")
        return vat_no.upper()


# Create Add Exclusions Form
class AddExclusionForm(forms.ModelForm):
    mandatory = forms.ChoiceField(
        required=False,
        widget=forms.widgets.Select(
            attrs={
                "placeholder": "Mandatory Exclusion Details",
                "class": "form-control",
            }
        ),
        choices=Exclusion.MANDATORY,
        label="",
    )
    discretionary = forms.ChoiceField(
        required=False,
        widget=forms.widgets.Select(
            attrs={
                "placeholder": "Discretionary Exclusion Details",
                "class": "form-control",
            }
        ),
        choices=Exclusion.DISCRETIONARY,
        label="",
    )
    exclusion_date = forms.DateField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Date of Exclusion ", "class": "form-control"}
        ),
        label="",
        validators=[
            MaxValueValidator(timezone.now().date()),
            MinValueValidator(
                timezone.now().date() - timezone.timedelta(days=365 * 10 + 3)
            ),
        ],
    )

    class Meta:
        model = Exclusion
        exclude = (
            "user",
            "supplier_id",
        )

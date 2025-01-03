from django.db import models
from django.core.exceptions import ValidationError


# Customer/Owner Model
class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


# Supplier Information Model
class Supplier(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    supplier_name = models.CharField(max_length=50)
    supplier_email = models.CharField(max_length=100)
    supplier_phone = models.CharField(max_length=15)
    supplier_address = models.CharField(max_length=50)
    supplier_city = models.CharField(max_length=50)
    supplier_country = models.CharField(max_length=50)
    supplier_postcode = models.CharField(max_length=10)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.supplier_name


# Supplier Details Model
class Detail(models.Model):
    COMPANY_TYPE = (
        ("Agricultural", "Agricultural"),
        ("Automotive", "Automotive"),
        ("Clothing & Accessories", "Clothing & Accessories"),
        ("Construction Materials", "Construction Materials"),
        ("Education & Training", "Education & Training"),
        ("Financial Services", "Financial Services"),
        ("Hospitality, Food & Beverage", "Hospitality, Food & Beverage"),
        ("IT Services", "IT Services"),
        ("Medical Equipment", "Medical Equipment"),
        ("Office Supplies", "Office Supplies"),
    )
    LEGAL_FORM = (
        ("Sole Trader", "Sole Trader"),
        ("Limited Company", "Limited Company"),
        ("Charity", "Charity"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    company_type = models.CharField(max_length=50, choices=COMPANY_TYPE)
    legal_form = models.CharField(max_length=50, choices=LEGAL_FORM)
    vat_no = models.CharField(max_length=20)
    supplier_id = models.OneToOneField(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.supplier_id.supplier_name} - {self.company_type} - {self.legal_form}"


# Supplier Exclusions Model
class Exclusion(models.Model):
    MANDATORY = (
        ("Theft", "Theft"),
        ("Fraud", "Fraud"),
        ("Bribery", "Bribery"),
        ("None", "None"),
    )
    DISCRETIONARY = (
        ("Bankruptcy", "Bankruptcy"),
        ("Improper Procurement", "Improper Procurement"),
        ("Breach of Contract", "Breach of Contract"),
        ("None", "None"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    mandatory = models.CharField(max_length=50, choices=MANDATORY)
    discretionary = models.CharField(max_length=50, choices=DISCRETIONARY)
    exclusion_date = models.DateField(null=True, blank=True)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def clean(self):
        if (
            self.mandatory != "None" or self.discretionary != "None"
        ) and self.exclusion_date is None:
            raise ValidationError(
                "Exclusion date is required if either mandatory or discretionary option is selected."
            )
        if (
            self.mandatory == "None"
            and self.discretionary == "None"
            and self.exclusion_date is not None
        ):
            raise ValidationError(
                "Exclusion date is not required if both mandatory and discretionary fields are None."
            )

    def __str__(self):
        return f"{self.supplier_id.supplier_name} - {self.mandatory} - {self.discretionary}"

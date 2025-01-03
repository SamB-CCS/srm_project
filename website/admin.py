from django.contrib import admin
from .models import Customer, Supplier, Detail, Exclusion

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Detail)
admin.site.register(Exclusion)

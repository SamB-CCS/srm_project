from django.urls import path
from django.contrib import admin
from . import views
from .views import MyWizardView

admin.site.site_header = "Supplier Relationship Management System Admin"

# URL paths for web application
urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register_user, name="register"),
    path("customer/<int:pk>", views.customer_record, name="customer"),
    path("update_customer/<int:pk>", views.update_customer, name="update_customer"),
    path("update_supplier/<int:pk>", views.update_supplier, name="update_supplier"),
    path("update_detail/<int:pk>", views.update_detail, name="update_detail"),
    path("update_exclusion/<int:pk>", views.update_exclusion, name="update_exclusion"),
    path("add_customer/", MyWizardView.as_view(), name="add_customer"),
    path("add_supplier/", MyWizardView.as_view(), name="add_supplier"),
    path("add_detail/", MyWizardView.as_view(), name="add_detail"),
    path("add_exclusion/", MyWizardView.as_view(), name="add_exclusion"),
    path("logout_confirm/", views.user_logout, name="user_logout"),
]

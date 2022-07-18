from django.urls import path
from .views import *

urlpatterns = [
    path("customer/stuff", CustomerViewSet.as_view({"get": "new_stuff"}), name="stuff"),
    path("customer/order", CustomerViewSet.as_view({"post": "place_order"}), name="place_order"),
    path("customer/table/assign", CustomerViewSet.as_view({"post": "assign_table"}), name="assign_table"),
    path("customer/<str:customer_id>/invoice", CustomerViewSet.as_view({"get": "generate_invoice"}), name="generate_invoice"),
    path("customer/<str:customer_id>/meal", CustomerViewSet.as_view({"get": "gets_meals"}), name="get_meal"),
]

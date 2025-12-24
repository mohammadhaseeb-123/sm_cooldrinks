from django.urls import path
from . import views

urlpatterns = [
    # Public landing page for customers
    path("", views.landing, name="landing"),

    # Auth + dashboard for shopkeeper
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="home"),

    # Inventory actions (login required)

    # ✅ DELETE must come BEFORE the generic action URL
    path("product/<int:product_id>/delete/", views.delete_product, name="delete_product"),

    # ✅ Generic increase / decrease
    path("product/<int:product_id>/<str:action>/", views.change_quantity, name="change_quantity"),
]

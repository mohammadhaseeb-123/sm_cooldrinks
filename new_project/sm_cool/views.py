from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category


def landing(request):
    """
    Public landing page for customers.
    Shows shop info, images, map, contact.
    No inventory data.
    """
    return render(request, "landing.html")


def user_login(request):
    """Login page for shopkeeper (and you)."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # /dashboard/
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("landing")


@login_required
def dashboard(request):
    """Inventory dashboard + add product form."""

    # Handle Add Product
    if request.method == "POST" and request.POST.get("form_type") == "add_product":
        name = request.POST.get("name")
        category_name = request.POST.get("category")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")

        if not all([name, category_name, price, quantity]):
            messages.error(request, "All fields are required.")
        else:
            try:
                quantity = int(quantity)
                price = Decimal(price)
            except ValueError:
                messages.error(request, "Price and quantity must be valid numbers.")
            else:
                category, _ = Category.objects.get_or_create(name=category_name)
                Product.objects.create(
                    name=name,
                    category=category,
                    price=price,
                    quantity=quantity,
                )
                messages.success(request, f"{name} added successfully!")
                return redirect("home")

    # Dashboard stats
    products = Product.objects.select_related("category").all().order_by("name")
    context = {
        "products": products,
        "total_products": products.count(),
        "total_stock": sum(p.quantity for p in products),
        "low_stock_items": products.filter(quantity__lt=10).count(),
        "categories_count": Category.objects.count(),
    }

    return render(request, "index.html", context)


@login_required
def change_quantity(request, product_id, action):
    """Increase or decrease stock quantity."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        if action == "inc":
            product.quantity += 1
        elif action == "dec" and product.quantity > 0:
            product.quantity -= 1
        product.save()

    return redirect("home")


@login_required
def delete_product(request, product_id):
    """
    Delete product (POST only).
    Works for superuser and client.
    """
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' deleted successfully.")

    return redirect("home")

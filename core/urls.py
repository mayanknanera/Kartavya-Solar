from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    # path("products/", views.products_view, name="products"),
    # path("solar-calculator/", views.solar_calculator, name="solar_calculator"),
    path("profile/", views.profile_view, name="profile"),
    # Product pages
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    # Cart
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", views.remove_cart_item, name="remove_cart_item"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
    # Checkout & Order
    path("checkout/", views.checkout, name="checkout"),
    path("order-success/", views.order_success, name="order_success"),
    path("orders/", views.orders_view, name="orders"),
    path("orders/<int:order_id>/", views.order_detail_view, name="order_detail"),
    path("orders/<int:order_id>/cancel/", views.cancel_order, name="cancel_order"),
]

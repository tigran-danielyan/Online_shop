from django.urls import path

from .views import (
    HomeView,
    checkout,
    ItemDetailView,
    OrderSummaryView,
    OrderListView,
    user_order_view,
    add_to_cart,
    remove_from_cart,
    decrease_item_quantity
)

app_name = "core"
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', checkout, name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),

    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('add_to_cart/<slug>/<str:user>',
         add_to_cart, name='add_to_cart-admin'),

    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_from_cart/<slug>/<str:user>',
         remove_from_cart, name='remove_from_cart-admin'),

    path('decrease_item_quantity/<slug>/',
         decrease_item_quantity, name='decrease_item_quantity'),
    path('decrease_item_quantity/<slug>/<str:user>',
         decrease_item_quantity, name='decrease_item_quantity-admin'),
    path("order-list/", OrderListView.as_view(), name="order-list"),
    path("order-list/<user>",
         user_order_view, name="user-order-view"),
]

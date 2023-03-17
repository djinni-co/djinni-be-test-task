from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wishlist', views.toggle_wish),
    path('add-wishlist', views.add_wishlist),
    path('wish-detailed', views.toggle_wish_detailed)
]


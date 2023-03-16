from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_wishlist', views.create_wishlist),
    path('get_wishlists', views.get_wishlists),
    path('update_wishlists', views.update_wishlists),
]


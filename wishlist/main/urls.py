from django.urls import path

from . import views

urlpatterns = [
    path('', views.ItemView.as_view(), name='index'),
    path('wishlist/', views.WishItemView.as_view()),
    path('wishcategory/', views.WishCategoryCreateView.as_view())
]

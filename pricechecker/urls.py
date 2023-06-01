from django.urls import path

from pricechecker import views

urlpatterns = [
    path('', views.search_form),
    path('search/', views.search_product, name='search'),
    path('prices/<int:pk>', views.get_prices, name='prices'),
]
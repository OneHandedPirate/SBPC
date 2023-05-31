from django.urls import path

from pricechecker.views import search_form, search_product, get_prices

urlpatterns = [
    path('', search_form, name='search'),
    path('search/', search_product, name='search'),
    path('prices/<int:pk>', get_prices, name='prices'),
]
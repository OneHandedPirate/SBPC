from django.urls import path

from pricechecker.views import search_form, search_product, get_prices

urlpatterns = [
    path('', search_form, name='search'),
    path('search/', search_product, name='search_results'),
    path('prices/', get_prices, name='prices'),
]
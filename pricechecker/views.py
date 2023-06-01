from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from pricechecker.models import Product, Price


def search_product(request):
    query = request.GET.get('q')
    product_list = []
    if query:
        product_list = Product.objects.filter(name__icontains=query)

    paginator = Paginator(product_list, 20)
    page_number = request.GET.get('page', None)

    if not page_number:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return render(request, 'pricechecker/search-results.html', {'products': page_obj, 'query': query})


def search_form(request):
    return render(request, template_name='pricechecker/default.html')


def get_prices(request, pk):
    product = Product.objects.get(pk=pk)
    results = Price.objects.filter(product_id=product).order_by('date')
    data = {
            'name': f'{product.name}',
            'prices': [{'price': result.price, 'date': result.date.strftime('%d.%m.%Y')} for result in results]
    }

    return JsonResponse(data)

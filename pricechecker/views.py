from django.http import JsonResponse
from django.shortcuts import render


from pricechecker.models import Product, Price


def search_product(request):
    query = request.POST.get('search-input')
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query)
    return render(request, 'pricechecker/search-results.html', {'products': results})


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

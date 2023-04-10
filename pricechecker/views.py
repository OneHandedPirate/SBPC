from django.http import JsonResponse
from django.shortcuts import render


from pricechecker.models import Product, Price


def search_product(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query)
    data = {
         'results': [{'name': result.name} for result in results]
     }

    return JsonResponse(data)


def search_form(request):
    return render(request, template_name='pricechecker/default.html')


def get_prices(request):
    q = request.GET.get('q')
    product = Product.objects.get(name=q)
    results = Price.objects.filter(product_id=product).order_by('date')
    data = {
            'name': f'{product.name}',
            'prices': [{'price': result.price, 'date': result.date.strftime('%d.%m.%Y')} for result in results]
    }

    return JsonResponse(data)
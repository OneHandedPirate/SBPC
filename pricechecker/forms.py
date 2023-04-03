from django.forms import ModelForm

from pricechecker.models import Product


class ProductForm(ModelForm):
    model = Product
    class Meta:
        fields = ('name',)
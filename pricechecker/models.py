from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Price(models.Model):
    product_id = models.ForeignKey(Product, related_name='price', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_id} {self.date}, {self.price}'
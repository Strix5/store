import stripe
from django.conf import settings
from django.db import models

from users.models import User

# Create your models here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'''{self.name}'''

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_product_price_id = models.CharField(max_length=128, blank=True, null=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'''Name: {self.name} | Category: {self.category}'''

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='usd'
        )
        return stripe_product_price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(map(lambda x: x.sum(), self))

    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self))

    def stripe_line_items(self):
        line_items = []
        for item in self:
            each = {
                'price': item.product.stripe_product_price_id,
                'quantity': item.quantity,
            }
            line_items.append(each)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'''Basket of {self.user.username} | Product: {self.product.name}'''

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return item

    # @classmethod
    # def create_or_update(cls, product, user):
    #     basket = Basket.objects.filter(user=user, product=product)
    #
    #     if not basket.exists():
    #         obj = Basket.objects.create(user=user, product=product, quantity=1)
    #         is_created = True
    #         return obj, is_created
    #     else:
    #         basket.quantity += 1
    #         basket.save()
    #         is_created = True
    #         return basket, is_created

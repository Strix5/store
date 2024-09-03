from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView

from common.views import CommonMixin

from .models import Basket, Product, ProductCategory


class IndexView(CommonMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(CommonMixin, ListView):
    template_name = 'products/products.html'
    model = Product
    paginate_by = 6
    context_object_name = 'products'
    title = 'Store-Catalog'

    def __init__(self, category_id=None, page_number=1):
        super().__init__()
        self.category_id = category_id
        self.page_number = page_number

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset



def product_view(request, product_id):
    context = {
        'product': Product.objects.get(id=product_id),
        'title': 'Product Info',
        }
    return render(request, 'products/product_info.html', context)


@login_required
def basket_add(request, product_id):
    # Basket.create_or_update(product_id, request.user)

    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

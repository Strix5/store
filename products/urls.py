from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', views.ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', views.ProductsListView.as_view(), name='paginator'),
    path('basket/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
    path('product_info/<int:product_id>/', views.product_view, name='product_view')
]

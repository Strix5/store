from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', login_required(views.OrdersListView.as_view()), name='orders'),
    path('order_create/', login_required(views.OrderCreateView.as_view()), name='order_create'),
    path('order/<int:pk>/', login_required(views.OrderView.as_view()), name='order'),
    path('order_success/', login_required(views.SuccessTemplateView.as_view()), name='order_success'),
    path('order_canceled', login_required(views.CanceledTemplateView.as_view()), name='order_canceled'),
]

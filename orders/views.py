from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import CommonMixin
from products.models import Basket

from .forms import OrderForm
from .models import Order

stripe.api_key = \
    'sk_test_51OQTYbBnyEYPA4JSPmzsWgIcte5qvezcyUrgnxnRywwvecQ6fn69ojn4gw6sw5dZ59Yr4JwB696Ey67jQwdG1U6p00brMa4zmm'

# Create your views here.


class OrdersListView(CommonMixin, ListView):
    title = 'Store - Orders'
    template_name = 'orders/orders.html'
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrdersListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderView(DetailView):
    template_name = 'orders/order.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['title'] = f'Заказ №{self.object.id}'
        return context


class SuccessTemplateView(CommonMixin, ListView):
    template_name = 'orders/success.html'
    title = 'Store - OrderSuccess'
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderCreateView(CommonMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = 'Store - OrderCreation'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_line_items(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=f'{settings.DOMAIN_NAME}{reverse('orders:order_success')}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse('orders:order_canceled')}',
        )
        return HttpResponseRedirect(checkout_session.url, HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    # TODO: fill me in
    order = Order.objects.get(id=order_id)
    order.update_after_payment()

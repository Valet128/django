from django.shortcuts import redirect
from .models import Product, Slide, Feedback
from .forms import PlacingAnOrderForm
from yookassa import Configuration, Payment
from django.views.generic import TemplateView, DetailView, FormView
from .utils import DataMixin
import uuid
from shvedovaav.settings import SHOP_ID, API_SECRET

class StoreHome(DataMixin, TemplateView):
    template_name = 'store/index.html'
    title = "АШАШ"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['slides'] = Slide.objects.all()
        context['feedbacks'] = Feedback.objects.all()
        return self.get_mixin_context(context)

class StoreProduct(DataMixin, DetailView):
    model = Product
    template_name = "store/product.html"
    pk_url_kwarg = 'id'
    context_object_name = 'product'
    allow_empty = False

class StorePlacingAnOrder(DataMixin, FormView, DetailView):
    form_class = PlacingAnOrderForm
    template_name = "store/placing_an_order.html"
    pk_url_kwarg = 'id'
    title = "Оформление заказа"

    def get_queryset(self):
        product = Product.objects.filter(pk=self.kwargs['id'])
        self.initial['amount'] = product[0].price
        self.initial['product_name'] = product[0].name
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def form_valid(self, form):
        Configuration.configure(SHOP_ID, API_SECRET)
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create(
                    {
                    "amount": {
                        "value": form.data['amount'],
                        "currency": "RUB",
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://shvedovaav.ru/thank_you",
                    },
                    "receipt": {
                        "customer": {
                            "email": form.data['customer_email'],
                            "phone": form.data['customer_phone'],
                        },
                        "items": [ 
                            {
                                "amount": {
                                    "value": form.data['amount'],
                                    "currency":"RUB",
                                },
                                
                                "quantity": 1,
                                "description": form.data['product_name'],
                                "vat_code": 1
                            },
                            ]
                    },
                    "capture": True,
                    },
                    idempotence_key)
        confirmation_url = payment.confirmation.confirmation_url
        return redirect(confirmation_url)

class StoreAccord(DataMixin, TemplateView):
    title = "Согласие с рассылкой"
    template_name = 'store/accord.html'

class StoreDenial(DataMixin, TemplateView):
    title = "Отказ от ответственности"
    template_name = 'store/denial.html'

class StoreConfidence(DataMixin, TemplateView):
    title = "Политика конфиденциальности"
    template_name = 'store/confidence.html'

class StoreTermOfUse(DataMixin, TemplateView):
    title = "Пользовательское соглашение"
    template_name = 'store/terms_of_use.html'

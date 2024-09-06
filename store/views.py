from django.shortcuts import redirect
from .models import Product, Slide, Feedback, Order
from .forms import PlacingAnOrderForm
from yookassa import Configuration, Payment
from django.views.generic import TemplateView, DetailView, FormView
from .utils import DataMixin
import uuid
from shvedovaav.settings import SHOP_ID, API_SECRET
import json
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

 


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
                        "return_url": "https://shvedovaav.ru/thank_you/",
                    },
                    "receipt": {
                        "customer": {
                            "email": form.data['customer_email'],
                            "phone": form.data['customer_phone'],
                            "full_name": form.data['customer_name'],
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


class StoreThankYou(DataMixin, TemplateView):
    title = "Спасибо за покупку"
    template_name = 'store/thank_you.html'


@csrf_exempt
def payment_result(request):
    
    if request.method == 'POST':
        try:
            event_json = json.loads(request.body)
            try:
                notification_object = WebhookNotification(event_json)
            except Exception:
                raise ValueError()
            payment = notification_object.object
            order = Order(
                amount = payment.amount.value,
                date = payment.created_at,
                customer_name = payment.metadata['full_name'],
                customer_email = payment.metadata['email'],
                customer_phone = payment.metadata['phone'],
                product = payment.description,
                token = payment.id,
                status = payment.status
            )
            
            if payment.status == 'succeeded':
                title_message1 = 'Оплата'
                text_message1 = f"{order.customer_name}, Оплата на сайте shvedovaav.ru прошла успешно!"
                email_to1 = [order.customer_email]

                email1 = EmailMessage(
                    subject=title_message1,
                    body=text_message1,
                    to=email_to1
                )
                email1.send()

                title_message2 = 'Оплата'
                text_message2 = f"""
                {order.customer_name}, оплатил курс - {order.product} на сумму {order.amount} RUB
                Номер телефона: {order.customer_phone}
                Почта: {order.customer_email}"""
                email_to2 = ['info@shvedovaav.ru']

                email2 = EmailMessage(
                    subject=title_message2,
                    body=text_message2,
                    to=email_to2
                )
                email2.send()
                order.save()

            elif payment.status == 'canceled':

                title_message2 = 'Оплата'
                text_message2 = f"""
                {order.customer_name}, отменил оплату - курс {order.product} на сумму {order.amount} RUB
                Номер телефона: {order.customer_phone}
                Почта: {order.customer_email}"""
                email_to2 = ['info@shvedovaav.ru']

                email2 = EmailMessage(
                    subject=title_message2,
                    body=text_message2,
                    to=email_to2
                )
                email2.send()
                order.save()

            elif payment.status == 'pending':

                title_message2 = 'Оплата'
                text_message2 = f"""
                {order.customer_name}, перешел к оплате - курс {order.product} на сумму {order.amount} RUB
                Номер телефона: {order.customer_phone}
                Почта: {order.customer_email}"""
                email_to2 = ['info@shvedovaav.ru']

                email2 = EmailMessage(
                    subject=title_message2,
                    body=text_message2,
                    to=email_to2
                )
                email2.send()
                
        except Exception as e:
            raise e

    return HttpResponse(request)


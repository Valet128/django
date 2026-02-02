from django.shortcuts import redirect
from .models import Product, Slide, Feedback, Order
from users.models import CustomUser
from yookassa import Configuration, Payment
from django.views.generic import TemplateView, DetailView, CreateView
from .utils import DataMixin
import uuid
from shvedovaav.settings import SHOP_ID, API_SECRET
import json
from django.http import HttpResponse, HttpResponseRedirect
from yookassa.domain.notification import WebhookNotification
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from users.forms import CourseCustomUserCreationForm, BookCustomUserCreationForm, FreeEventCustomUserCreationForm


class StoreHome(DataMixin, TemplateView):
    template_name = 'store/index.html'
    title = "АШАШ"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-id')[:3]
        context['slides'] = Slide.objects.all()
        context['feedbacks'] = Feedback.objects.all()
        return self.get_mixin_context(context)



class StoreProduct(DataMixin, DetailView):
    model = Product
    template_name = "store/product.html"
    pk_url_kwarg = 'id'
    context_object_name = 'product'
    allow_empty = False
    
class StoreFreeEvent(DataMixin, CreateView, DetailView):
    template_name = "store/free_event.html"
    pk_url_kwarg = 'id'
    title = "Запись на мероприятие"
    form_class = FreeEventCustomUserCreationForm

    def get_queryset(self):
        product = Product.objects.filter(pk=self.kwargs['id'])
        self.initial['product_name'] = product[0].name
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
    
    def form_valid(self, form):
        product = Product.objects.filter(pk=self.kwargs['id'])
        if product[0].link == None or product[0].link == '':
            success_url = 'https://shvedovaav.ru/success_for_event'
        success_url = product[0].link
        client = CustomUser.objects.filter(email=form.cleaned_data['email'])
        if not client:
            user = form.save()
            
            user.phone = form.cleaned_data['customer_phone']
            user.first_name = form.cleaned_data['customer_firstname']
            user.ip_address = self.request.META.get('REMOTE_ADDR')
            user.personal_data_accepted = form.cleaned_data['personal_data_accepted']
            user.send_messages_accepted = form.cleaned_data['send_messages_accepted']
            user.users_agreement_accepted = form.cleaned_data['users_agreement_accepted']
           
            form.save()

            title_message = 'Регистрация'
            text_message = f"""
{form.cleaned_data['customer_firstname']}, Вы зарегистрировались на сайте shvedovaav.ru!
Ваш пароль {form.cleaned_data['password1']}
Смените ваш пароль для большей безопасности в профиле https://shvedovaav.ru/users/profile

Это письмо пришло к вам, так как вы подписаны на рассылку рекламных и информационных сообщений.
Если данное письмо пришло к вам по ошибке, просто проигнорируйте данное сообщение.

Вы можете отозвать согласие на обработку персональных данных и рассылку сообщений на странице: https://shvedovaav.ru/users/profile
Или написав нам на почту: info@shvedovaav.ru
Или позвонив по телефону: +7-906-911-59-88
"""
            email_to = [form.cleaned_data['email']]

            email = EmailMessage(
                subject=title_message,
                body=text_message,
                to=email_to
            )
            email.send()

        title_message_self = 'Новая запись на бесплатное мероприятие'
        text_message_self = f"""
Пользователь {form.cleaned_data['customer_firstname']} записался на мероприятие {form.cleaned_data['product_name']}!
Номер телефона: {form.cleaned_data['customer_phone']}
Email: {form.cleaned_data['email']}

Это письмо пришло к вам, так как вы подписаны на рассылку рекламных и информационных сообщений.

Вы можете отозвать согласие на обработку персональных данных и рассылку сообщений на странице: https://shvedovaav.ru/users/profile
Или написав нам на почту: info@shvedovaav.ru
Или позвонив по телефону: +7-906-911-59-88
"""
        email_to_self = ['info@shvedovaav.ru']

        email_self = EmailMessage(
            subject=title_message_self,
            body=text_message_self,
            to=email_to_self
        )
        email_self.send()

        title_message_client = 'Запись на мероприятие'
        text_message_client = f"""
Здравствуйте, {form.cleaned_data['customer_firstname']} вы записались на мероприятие {form.cleaned_data['product_name']}!
Ссылка на мероприятие: {success_url}

Это письмо пришло к вам, так как вы подписаны на рассылку рекламных и информационных сообщений.

Вы можете отозвать согласие на обработку персональных данных и рассылку сообщений на странице: https://shvedovaav.ru/users/profile
Или написав нам на почту: info@shvedovaav.ru
Или позвонив по телефону: +7-906-911-59-88
"""
        email_to_client = [form.cleaned_data['email']]

        email_client = EmailMessage(
            subject=title_message_client,
            body=text_message_client,
            to=email_to_client
        )
        email_client.send()

        return redirect(success_url)
    




class StorePlacingAnOrder(DataMixin, CreateView, DetailView):
    template_name = "store/placing_an_order.html"
    pk_url_kwarg = 'id'
    title = "Оформление заказа"

    def get_form_class(self):
        product = Product.objects.filter(pk=self.kwargs['id'])
        if str(product[0].category) == 'Книга':
            self.form_class = BookCustomUserCreationForm
        else:
            self.form_class = CourseCustomUserCreationForm
        
        return self.form_class
    
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

        client = CustomUser.objects.filter(email=form.cleaned_data['email'])
        if not client:
            user = form.save()
            
            if isinstance(form, BookCustomUserCreationForm):
                user.last_name = form.cleaned_data['customer_lastname']
                user.middle_name = form.cleaned_data['customer_middlename']
                user.address = form.cleaned_data['customer_address']

            user.phone = form.cleaned_data['customer_phone']
            user.first_name = form.cleaned_data['customer_firstname']
            user.ip_address = self.request.META.get('REMOTE_ADDR')
            user.personal_data_accepted = form.cleaned_data['personal_data_accepted']
            user.send_messages_accepted = form.cleaned_data['send_messages_accepted']
            user.users_agreement_accepted = form.cleaned_data['users_agreement_accepted']
            form.save()

            title_message = 'Регистрация'
            text_message = f"""
{form.cleaned_data['customer_firstname']}, Вы зарегистрировались на сайте shvedovaav.ru!
Ваш пароль {form.cleaned_data['password1']}
Смените ваш пароль для большей безопасности в профиле https://shvedovaav.ru/users/profile

Это письмо пришло к вам, так как вы подписаны на рассылку рекламных и информационных сообщений.
Если данное письмо пришло к вам по ошибке, просто проигнорируйте данное сообщение.

Вы можете отозвать согласие на обработку персональных данных и рассылку сообщений на странице: https://shvedovaav.ru/users/profile
Или написав нам на почту: info@shvedovaav.ru
Или позвонив по телефону: +7-906-911-59-88
"""
            email_to = [form.cleaned_data['email']]

            email = EmailMessage(
                subject=title_message,
                body=text_message,
            to=email_to
            )
            email.send()
            
            if isinstance(form, CourseCustomUserCreationForm):
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
                            "metadata":{
                                "name": form.data['customer_firstname'],
                                "email": form.data['email'],
                                "phone": form.data['customer_phone'],
                                "product_name": form.data['product_name'],
                                "address": 'None',
                            },
                            "receipt": {
                                "customer": {
                                    "email": form.data['email'],
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
            else:
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
                    "metadata":{
                        "name": form.data['customer_lastname'] + " " + form.data['customer_firstname'] + " " + form.data['customer_middlename'],
                        "email": form.data['email'],
                        "phone": form.data['customer_phone'],
                        "product_name": form.data['product_name'],
                        "address": form.data['customer_address'],
                    },
                    "receipt": {
                        "customer": {
                            "email": form.data['email'],
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
            
        else:
            
            
            if isinstance(form, CourseCustomUserCreationForm):
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
                            "metadata":{
                                "name": form.data['customer_firstname'],
                                "email": form.data['email'],
                                "phone": form.data['customer_phone'],
                                "product_name": form.data['product_name'],
                                "address": 'None',
                            },
                            "receipt": {
                                "customer": {
                                    "email": form.data['email'],
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
            else:
                user = CustomUser.objects.get(email=form.cleaned_data['email'])
                if user.last_name == None:
                    user.last_name = form.cleaned_data['customer_lastname']
                if user.middle_name == None:
                    user.middle_name = form.cleaned_data['customer_middlename']
                if user.address == None:
                    user.address = form.cleaned_data['customer_address']
                user.save()
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
                    "metadata":{
                        "name": form.data['customer_lastname'] + " " + form.data['customer_firstname'] + " " + form.data['customer_middlename'],
                        "email": form.data['email'],
                        "phone": form.data['customer_phone'],
                        "product_name": form.data['product_name'],
                        "address": form.data['customer_address'],
                    },
                    "receipt": {
                        "customer": {
                            "email": form.data['email'],
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

class StoreAccordPD(DataMixin, TemplateView):
    title = "Согласие на обработку персональных данных"
    template_name = 'store/accord_pd.html'

class StoreAccordTTP(DataMixin, TemplateView):
    title = "Согласие на передачу персональных данных третьим лицам"
    template_name = 'store/accord_ttp.html'


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

class StoreSuccessForEvent(DataMixin, TemplateView):
    title = "Спасибо за покупку"
    template_name = 'store/success_for_event.html'


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
                customer_name = payment.metadata['name'],
                customer_email = payment.metadata['email'],
                customer_phone = payment.metadata['phone'],
                product = payment.metadata['product_name'],
                address = payment.metadata['address'],
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

def accept_cookies(request):
    id = uuid.uuid4()
    response = HttpResponseRedirect('/')
    age = 3600*24*365
    response.set_cookie('shvedovaav_cookie', id, max_age=age)
    return response
from django.core import serializers

def get_products(request):
    products = list(Product.objects.all().order_by('-id'))
    data = serializers.serialize('json', products)
    return HttpResponse(data, content_type='application/json')
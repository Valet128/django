from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreHome.as_view(), name='home'),
    path('get_products', views.get_products, name='get_products'),
    path('accord', views.StoreAccord.as_view(), name='accord'),
    path('accord_pd', views.StoreAccordPD.as_view(), name='accord_pd'),
    path('accord_ttp', views.StoreAccordTTP.as_view(), name='accord_ttp'),
    path('denial', views.StoreDenial.as_view(), name='denial'),
    path('confidence', views.StoreConfidence.as_view(), name='confidence'),
    path('terms_of_use', views.StoreTermOfUse.as_view(), name='terms_of_use'),
    path('placing_an_order/<int:id>/', views.StorePlacingAnOrder.as_view(), name='placing_an_order'),
    path('free_event/<int:id>/', views.StoreFreeEvent.as_view(), name='free_event'),
    path('product/<int:id>/', views.StoreProduct.as_view(), name='product'),
    path('thank_you/', views.StoreThankYou.as_view(), name='thank_you'),
    path('success_for_event/', views.StoreSuccessForEvent.as_view(), name='success_for_event'),
    path('payment_result/', views.payment_result, name='payment_result'),
    path('accept_cookies/', views.accept_cookies, name='accept_cookies'),
]
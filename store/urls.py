from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreHome.as_view(), name='home'),
    path('accord', views.StoreAccord.as_view(), name='accord'),
    path('denial', views.StoreDenial.as_view(), name='denial'),
    path('confidence', views.StoreConfidence.as_view(), name='confidence'),
    path('terms_of_use', views.StoreTermOfUse.as_view(), name='terms_of_use'),
    path('placing_an_order/<int:id>/', views.StorePlacingAnOrder.as_view(), name='placing_an_order'),
    path('product/<int:id>/', views.StoreProduct.as_view(), name='product'),
    path('thank_you/', views.StoreThankYou.as_view(), name='thank_you'),
    path('payment_result/', views.payment_result, name='payment_result'),
]
from django.contrib import admin
from django.urls import path
from store import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.StoreHome.as_view()),
    path('accord', views.StoreAccord.as_view(), name='accord'),
    path('denial', views.StoreDenial.as_view(), name='denial'),
    path('confidence', views.StoreConfidence.as_view(), name='confidence'),
    path('terms_of_use', views.StoreTermOfUse.as_view(), name='terms_of_use'),
    path('placing_an_order/<int:id>/', views.StorePlacingAnOrder.as_view(), name='placing_an_order'),
    path('product/<int:id>/', views.StoreProduct.as_view(), name='product'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

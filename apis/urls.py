from django.urls import path, include

urlpatterns = [
    path('auth/', include('apis.authentication.urls')),
    path('plans/', include('apis.plans.urls')),
    path('customer/', include('apis.customer.urls')),
    path('brand/', include('apis.brand.urls')),
]
from django.urls import path, include

urlpatterns = [
    path('v1/', include('apis.brand.v1.urls')),
]
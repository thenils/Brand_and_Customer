from django.urls import path, include

urlpatterns = [
    path('v1/', include('apis.customer.v1.urls'))
]
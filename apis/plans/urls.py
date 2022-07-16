from django.urls import path, include

urlpatterns = [
    path('v1/', include('apis.plans.v1.urls'))
]
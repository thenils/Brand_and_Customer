from django.urls import path, include

urlpatterns = [
    path('v1/', include('apis.authentication.v1.urls'))
]
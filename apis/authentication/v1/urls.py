from django.urls import path
from rest_framework.routers import DefaultRouter

from apis.authentication.v1.views import RegisterView, LogoutView, AuthView

router = DefaultRouter()
router.register('', AuthView, basename='auth_view')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
urlpatterns += router.urls

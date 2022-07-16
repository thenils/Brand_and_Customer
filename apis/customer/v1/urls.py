from django.urls import path, include

from apis.customer.v1.views import CustomerGoalViewSet

urlpatterns = [
    path('goals/', CustomerGoalViewSet.as_view(), name='customer_goals'),
]
from django.urls import path, include

from apis.plans.v1.views import PlanListView, PromotionListView

urlpatterns = [
    path('plans/', PlanListView.as_view({'get': 'list'}), name='list_plans'),
    path('promotions/', PromotionListView.as_view({'get': 'list'}), name='list_promotions')
]
from django.urls import path, include

from apis.brand.v1.views import PlanViewSet, PromotionViewSet

urlpatterns = [
    path('plans/', PlanViewSet.as_view({'get': 'list', 'post': 'create'}), name='plan-list'),
    path('plan/<str:plan_id>/', PlanViewSet.as_view({'get': 'retrieve'}), name='plan-detail'),
    path('promotions/<str:plan_id>/', PromotionViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='promotion-list'),
    path('promotion/<str:promotion_id>/', PromotionViewSet.as_view({'get': 'retrieve'}), name='promotion-details'),
]

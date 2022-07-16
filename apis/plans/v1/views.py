from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apis.plans.v1.serializer import PlanReadOnlySerializer, PromotionReadOnlySerializer
from brand.models import Plan, Promotion
from modules.pagination import get_paginated_response


class PlanListView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        """
            List all the active plans
        """
        queryset = Plan.objects.filter(is_active=True)
        if not queryset:
            return Response({'message': 'No Active Plan Available'})
        return get_paginated_response(
            pagination_class=PageNumberPagination,
            serializer_class=PlanReadOnlySerializer,
            queryset=queryset,
            request=request,
            view=self
        )


class PromotionListView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        """
            List all the active plans
        """
        queryset = Promotion.objects.filter(is_active=True)
        if not queryset:
            return Response({'message': 'No Active Promotion Available'})
        return get_paginated_response(
            pagination_class=PageNumberPagination,
            serializer_class=PromotionReadOnlySerializer,
            queryset=queryset,
            request=request,
            view=self
        )

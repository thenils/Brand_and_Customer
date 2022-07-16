from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from brand.models import Plan,Promotion
from rest_framework.response import Response

from apis.brand.v1.serializer import PlanReadOnlySerializer, PlanDetailsSerializer, PlanCreateSerializer, \
    PromotionDetailSerializer, PromotionCreateSerializer
from apis.plans.v1.serializer import PromotionReadOnlySerializer
from modules.pagination import get_paginated_response


class PlanViewSet(viewsets.GenericViewSet):
    """
        viewset  for listing/ retrieving and creating brand plan details
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        """
            List all the active plans
        """
        user = request.user
        queryset = Plan.objects.filter(brand__user__id=user.id, is_active=True)
        return get_paginated_response(
            pagination_class=PageNumberPagination,
            serializer_class=PlanReadOnlySerializer,
            queryset=queryset,
            request=request,
            view=self
        )

    def retrieve(self, request, plan_id):
        """
            Retrieve a plan details by plan_id
        """
        user = request.user
        qs = get_object_or_404(Plan, pk=plan_id)
        serializer = PlanDetailsSerializer(qs)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = PlanCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.data)
        return Response(
            {
                'success': True,
                'message': "new plan added successfully",
            },
            status=status.HTTP_201_CREATED
        )


class PromotionViewSet(viewsets.GenericViewSet):
    """
        viewset  for listing/ retrieving and creating brand plan details
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request, plan_id):
        """
            list all promotions for a plan
        """

        queryset = Promotion.objects.filter(plan_id=plan_id, is_active=True)
        return get_paginated_response(
            pagination_class=PageNumberPagination,
            serializer_class=PromotionReadOnlySerializer,
            queryset=queryset,
            request=request,
            view=self
        )

    def retrieve(self, request, promotion_id):
        """
            retrieve a promotion by promotion_id
        """
        qs = get_object_or_404(Promotion, pk=promotion_id)
        serializer = PromotionDetailSerializer(qs)
        data = serializer.data
        return Response(data ,status=status.HTTP_200_OK)

    def create(self, request, plan_id):
        """
            create a promotion
        """
        data = request.data
        serializer = PromotionCreateSerializer(data=data, context={'plan_id': plan_id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {
                'success':True,
                'message':f"new promotion added : {request.data.get('promotion_name')}",
                'plan_name' : request.data.get('promotion_name'),
                'id' : serializer.data.get('id')

            },
            status= status.HTTP_201_CREATED
        )

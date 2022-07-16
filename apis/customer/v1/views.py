from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from customer.models import CustomerGoal

from apis.customer.v1.serializer import CustomerWOSerializer, CustomerGoalReadOnlySerializer
from modules.pagination import get_paginated_response

from django.core import serializers
class CustomerGoalViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self,request):
        """
        List all the customer Goals
        """
        user = request.user
        queryset = CustomerGoal.objects.filter(is_active=True)
        return get_paginated_response(
            pagination_class=PageNumberPagination,
            serializer_class=CustomerGoalReadOnlySerializer,
            queryset=queryset,
            request=request,
            view=self
        )

    def post(self, request):
        """
        create customer goals
        """
        serializer = CustomerWOSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            print(serializer.data)
            serializer.create(validate_data=serializer.data)
            return Response({'status': True})
        return Response({'status': False})

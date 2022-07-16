from django.contrib.auth import logout
from django.http import HttpResponse
from rest_framework import status, generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.authentication.v1.serializer import RegisterSerializer, LoginSerializer
from modules.errors import ERRORS


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        return context


class AuthView(viewsets.GenericViewSet):
    """
        A viewset that provides the standard actions
    """
    authentication_classes = ()
    permission_classes = ()

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['post'])
    def login(self, request):
        self.serializer_class = self.get_serializer_class()
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        is_valid = serializer.is_valid(raise_exception=False)
        if not is_valid:
            return Response(ERRORS["NO_USER"], status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        res = HttpResponse(status=status.HTTP_200_OK, content_type='application/json')
        try:
            res.delete_cookie('session_id')
            res.delete_cookie('x-token')
        except Exception as e:
            print(e.args)
        return res

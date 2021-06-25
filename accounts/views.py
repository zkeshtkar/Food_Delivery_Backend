from rest_framework import generics, decorators
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accounts import transactions
from accounts.models import User
from accounts.serializers import RegisterWithEmailSerializer, RegisterWithPhoneSerializer
from utilities import exceptions as authnz_exceptions
from rest_framework import exceptions


class RegisterWithEmailView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    """
    Register with email and password pass min len is 8 and need alpha and numeric
    """
    serializer_class = RegisterWithEmailSerializer

    def post(self, request, **kwargs):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                email = serialized_data.data['email'].lower()
                password = request.data['password']
                try:
                    user = User.objects.get(email=email)

                except User.DoesNotExist as e:
                    user = None
                if user:
                    raise authnz_exceptions.CustomException(detail='This email is registered before.')
                else:
                    RegisterWithEmailSerializer(data=request.data)
                    transactions.register_user_with_email_and_password(email, password)
                    return Response(status=status.HTTP_200_OK)
        except authnz_exceptions.CustomException as e:
            return Response(status=e.status_code)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)


class RegisterWithPhoneView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]

    """
    Register with email and password pass min len is 8 and need alpha and numeric
    """
    serializer_class = RegisterWithPhoneSerializer

    def post(self, request, **kwargs):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                phone = serialized_data.data['phone']
                pass_word = request.data['password']
                try:
                    user = User.objects.get(phone=phone)

                except User.DoesNotExist as e:
                    user = None

                if user:
                    raise authnz_exceptions.CustomException(detail='This phone is registered before.')
                else:
                    RegisterWithPhoneSerializer(data=request.data)
                    transactions.register_user_with_phone_and_password(phone, pass_word)
                    return Response(status=status.HTTP_200_OK)
        except authnz_exceptions.CustomException as e:
            return Response(status=e.status_code)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)


class LogoutAPIView(APIView):
    permission_classes = [AllowAny, ]

    pass

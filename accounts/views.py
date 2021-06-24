from django.contrib.auth import authenticate
from rest_framework import generics, decorators
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from accounts import transactions
from accounts.models import User
from accounts.serializers import RegisterWithEmailSerializer, RegisterWithPhoneSerializer
from utilities import responses, exceptions as authnz_exceptions, utilities
from rest_framework import exceptions


class RegisterWithEmailView(generics.CreateAPIView):

    permission_classes = [AllowAny, ]
    """
    Register with email and password pass min len is 8 and need alpha and numeric
    """
    serializer_class = RegisterWithEmailSerializer

    def post(self, request, **kwargs):
        try:
            print(request.data)
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
                    return responses.SuccessResponse(message='Registration completed successfully.').send()
        except authnz_exceptions.CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
        except exceptions.ValidationError as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()


@decorators.authentication_classes([])
@decorators.permission_classes([])
class RegisterWithPhoneView(generics.CreateAPIView):
    """
    Register with email and password pass min len is 8 and need alpha and numeric
    """
    serializer_class = RegisterWithPhoneSerializer

    def post(self, request, **kwargs):
        try:
            print(request)
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
                    return responses.SuccessResponse(message='Registration completed successfully').send()
        except authnz_exceptions.CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
        except exceptions.ValidationError as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()


class LogoutAPIView(APIView):
    pass

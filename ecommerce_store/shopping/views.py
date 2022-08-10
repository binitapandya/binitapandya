import re
from .models import  User
from shopping.serializers import UserRegistrationSerializer, UserLoginSerializer, StoreSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
import json
# Create your views here.

# Generate Manual Token Code Start #
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      
  }


class UserRegistrationView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self, request, format=None):
        serializer = ''
        try:
            serializer = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            pass

        password = make_password(request.data.pop("password"))
        request.data["password"] = password

        serializer = UserRegistrationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            token = get_tokens_for_user(user)
            
            user = User.objects.get(email=user)
    
            print(user)
            country = ''
            birthdate = ''
            
            if user.country != '':
                country = user.country
            else:
                country = None

            if user.birthdate != '':
                birthdate = user.birthdate
            else:
                birthdate = None

           
            User_data = {
                'id':user.id,
                'firstname':user.firstname,
                'lastname':user.lastname,
                'email':user.email,
                'mobile':user.mobile,
                'gender':user.gender,
                'country':country,
                'birthdate':birthdate,
                'password':password,
                'is_active':user.is_active,
                'is_admin':user.is_admin,
                'is_store_admin':user.is_store_admin,
                'country_code':user.country_code,
                'access_token':token.get('access'),
                'refresh_token':token.get('refresh'),
            }
            return Response({"status":True, "message":"Register Successfully", "data":User_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":False, "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# User Registration Api Code End #  

class LoginView(APIView):
    # renderer_classes = [UserRenderer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                try:
                    user = User.objects.get(email=serializer.data.get('email'))
                except User.DoesNotExist:
                    return Response({"status":"false", "message":"User Detail Not Found"}, status=status.HTTP_404_NOT_FOUND)

                User_data = {
                    'email':user.email,
                    'access_token':token.get('access'),
                    'refresh_token':token.get('refresh')
                }
                return Response({"status":True, "message":"Login Successfully", "data":User_data}, status=status.HTTP_200_OK)
            else:
                return Response({"status":"false", "message":{"non_field_errors":["Email or Password is not valid"]}}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status":"false", "message":"Some Fields Are Missing"}, status=status.HTTP_400_BAD_REQUEST)
# User Login Api Code End #

class StoreView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request , format=None):
        print(request.user)
        try:
            user = User.objects.get(email=str(request.user))
        except:
            return Response({"status":False, "message":"User Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        # print(user)
        # print(request.data, "before add user")
        # request.data["user"] = user.id
        # print(request.data, "after add user")
        if user.is_store_admin:
            serializer = StoreSerializer(data=request.data, context={"request":request})
            # serializer = StoreSerializer(user,data=request.data)
            # print(serializer)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
        
                return Response({"status":True, "message":"created successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status":False,  "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
             return Response({"status":False,  "message":"customer cann't add store"}, status=status.HTTP_400_BAD_REQUEST)    
# student end #                 
from pyexpat import model
from typing import ValuesView
from rest_framework import serializers
from shopping.models import Store, User

class UserRegistrationSerializer(serializers.ModelSerializer):
    ''' User Register by firstname, lastname, email, mobile, gender, country, birthdate, is_agree,
    registered_by,  password. Here, country and birthdate is optional fields'''
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'mobile', 'country', 'birthdate', 'gender', 'is_store_admin', 'password', 'country_code','created_at','modified_at']
        extra_kwargs={
            'password':{'write_only':True},
            'country':{'required':False},
            'birthdate':{'required':False},
            "modified_at":{'required':False}
        }
    
    def create(self, validate_data):
        # print(validate_data)
        return User.objects.create(**validate_data)
# Registration Serializer Code End #

# Login Serializer Code Start #
class UserLoginSerializer(serializers.ModelSerializer):
    ''' User Login by email and password '''
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
# Login Serializer Code End # 


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"
        extra_kwargs={
            'user':{'required':False},  
        }
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return Store.objects.create(**validated_data)
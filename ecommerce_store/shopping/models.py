from __future__ import unicode_literals
import email
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,  firstname, lastname, email, mobile, country, birthdate, gender,is_store_admin, password=None):
        """
        Creates and saves a User with the given email, mobile, gender and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

    
        user = self.model(
            email=self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            mobile = mobile,
            country = country,
            birthdate = birthdate,
            gender = gender,
            is_store_admin=is_store_admin
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
        

   
    def create_superuser(self, firstname, lastname, email, mobile, country, birthdate, gender, is_store_admin ,password):
        
        user = self.create_user(
            email=email,
            password=password,
            mobile=mobile,
            gender=gender,
            country=country,
            firstname=firstname,
            lastname=lastname,
            birthdate=birthdate,
            is_store_admin=is_store_admin
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255, default="", blank=True, null=True)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    mobile = models.CharField(max_length=255, default="", blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.CharField(default='', blank=True, null=True, max_length=255)
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES) 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    country_code = models.CharField(max_length=5, default="", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    is_store_admin = models.BooleanField(default=False)
    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'mobile', 'country', 'birthdate', 'gender','is_store_admin']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Store(models.Model):
    user=models.ForeignKey(User, related_name='user_store', on_delete=models.CASCADE)
    store_name=models.CharField(max_length=255)
    contact=models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    zip_code=models.CharField(max_length=255)
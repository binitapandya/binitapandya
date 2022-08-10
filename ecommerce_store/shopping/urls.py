from django.urls import path, re_path
from . import views 
urlpatterns = [
    path('registrat/', views.UserRegistrationView.as_view(), name='registrat'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('store/', views.StoreView.as_view(), name='store'),


]


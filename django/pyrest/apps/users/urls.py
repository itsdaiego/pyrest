from django.urls import path
from . import views


urlpatterns = [
    path('users', views.create_user, name='create_user'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
]

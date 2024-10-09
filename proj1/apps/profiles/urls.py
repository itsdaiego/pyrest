from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.get),
    path('profiles', views.post)
]

from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.create_job, name='create_job'),
]
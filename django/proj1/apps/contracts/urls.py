

from django.urls import path
from . import views


urlpatterns = [
    path('jobs/', views.create_contract, name='create_job')
]



from django.urls import path
from . import views


urlpatterns = [
    path('contracts/', views.create_contract, name='create_contract')
]

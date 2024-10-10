from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.create_job, name='create_job'),
    path('jobs/<int:job_id>/pay/', views.perform_payment, name='perform_payment'),
]

from django.db import models
from rest_framework.decorators import api_view

from proj1.apps.contracts.models import Contract



class Job(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    price = models.IntegerField()
    paid = models.BooleanField()
    payment_date = models.DateTimeField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description}"


from django.db import models


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    price = models.IntegerField()
    paid = models.BooleanField()
    payment_date = models.DateTimeField()
    #contract_id

    def __str__(self):
        return f"{self.description}"


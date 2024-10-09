from django.db import models

from proj1.apps.profiles.models import Profile


class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client')
    contractor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='contractor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contract {self.id}"

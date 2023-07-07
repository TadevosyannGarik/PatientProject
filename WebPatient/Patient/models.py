from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    date_added = models.DateTimeField(null=True)
    diagnosis = models.TextField(max_length=255)
    blood_type = models.TextField(max_length=25)


    def __str__(self):
        return self.username
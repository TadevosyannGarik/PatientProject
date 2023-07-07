from django.contrib.auth.models import User
from .models import Patient


def save_date(first_name, last_name, email, password):
    user = User.objects.create_user(username=email, password=password, email=email)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    Patient.objects.create(user=user)
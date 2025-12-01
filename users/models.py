from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

# Custom User model
class Users(AbstractUser):
    phone = PhoneNumberField(max_length=15, blank=True, null=True, unique=True)
    address = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Skill(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.skill_name}"



def validate_pdf(file):
    if not file.name.lower().endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")

class CV(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='cv')
    cv_file = models.FileField(upload_to='cvs/', validators=[validate_pdf])

    def __str__(self):
        return f"{self.user.username}'s CV"

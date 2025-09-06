from datetime import timedelta
from django.utils import timezone
from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    pass

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    def is_expired(self):
        # ✅ Django timezone ka use
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"OTP({self.code}) for {self.user}"

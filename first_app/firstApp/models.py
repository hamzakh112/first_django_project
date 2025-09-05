from django.db import models 
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):

        pass
class Blog(models.Model):   # ✅ Use PascalCase
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title
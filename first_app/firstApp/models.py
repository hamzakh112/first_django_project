from django.db import models

class Blog(models.Model):   # ✅ Use PascalCase
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
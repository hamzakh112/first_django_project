from django.contrib import admin
from .models import Blog ,User  # ✅ Use capital B

admin.site.register(Blog)
admin.site.register(User)


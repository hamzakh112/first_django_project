from django.contrib import admin
from .models import Blog   # ✅ Use capital B

admin.site.register(Blog)

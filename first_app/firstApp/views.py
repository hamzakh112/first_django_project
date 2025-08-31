from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .models import blog

def index(request):
    return render(request, 'index.html')
USERS = {}

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
       

        if not username or not password:
            messages.error(request, "Username aur password zaroori hain.")
            return render(request, 'signup.html')

        if username in USERS:  # check without DB
            messages.error(request, "Ye username already taken hai.")
            return render(request, 'signup.html')

        # Save in dict instead of DB
        USERS[username] = password
        print(username, password)
        messages.success(request, "Account ban gaya! Ab login karein.")
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # check from USERS dict
        if username in USERS and USERS[username] == password:
            request.session['user'] = username  # save in session
            messages.success(request, f"Welcome {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def dashboard_view(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')

    # users_list = [
    #     {"name": "Hamza", "age": 28, "email": "hamza@email.com", "number": "03001234567"},
    #     {"name": "Ali", "age": 25, "email": "ali@email.com", "number": "03111234567"},
    #     {"name": "Ayesha", "age": 21, "email": "ayesha@email.com", "number": "03211234567"},
    #     {"name": "Usman", "age": 30, "email": "usman@email.com", "number": "03331234567"},
    #     {"name": "Zara", "age": 23, "email": "zara@email.com", "number": "03451234567"},
    #     {"name": "Bilal", "age": 27, "email": "bilal@email.com", "number": "03561234567"},
    # ]

    # context = {
    #     "username": user,
    #     "users": users_list
    # }

    return render(request, "dashboard.html", )

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')
def DashboardView(View):
 class DashboardView(View):
    def get(self, request):
      blogs=blogs.objects.all()
      context={'blogs':blogs}
      return render(request, 'dashboard.html', context)
class BlogDetailView(View):
    def get(self, request, ):
        return render(request, 'blog.html')
class DashboardView(View):
    def get(self, request):
        blogs = blog.objects.all()
        context = {'blogs': blogs}
        return render(request, 'dashboard.html', context)


class BlogDetailView(View):
    def get(self, request, blog_id):
        single_blog = blog.objects.get(id=blog_id)
        context = {'blog': single_blog}
      
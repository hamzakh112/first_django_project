from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from .models import Blog

USERS = {}  # temporary storage without DB

def index(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Username aur password zaroori hain.")
            return render(request, 'signup.html')

        if username in USERS:
            messages.error(request, "Ye username already taken hai.")
            return render(request, 'signup.html')

        USERS[username] = password
        messages.success(request, "Account ban gaya! Ab login karein.")
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if username in USERS and USERS[username] == password:
            request.session['user'] = username
            messages.success(request, f"Welcome {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def dashboard_view(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')

    blogs = Blog.objects.all().order_by('-created_at')

    context = {
        "username": user,
        "blogs": blogs
    }
    return render(request, "dashboard.html", context)

def blog_detail_view(request, blog_id):
    single_blog = get_object_or_404(Blog, id=blog_id)
    return render(request, "blog.html", {"blog": single_blog})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')

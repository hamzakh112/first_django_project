from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Blog
from django.contrib.auth import get_user_model
User = get_user_model()

# Home page
def index(request):
    return render(request, 'index.html')


# Signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        print(username, first_name, email, password)

        if not username or not password:
            messages.error(request, "Username aur password zaroori hain.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ye username already taken hai.")
            return render(request, 'signup.html')
        #Djano database 
        User.objects.create_user(
            username=username,
            first_name=first_name,
            email=email,
            password=password
        )

        messages.success(request, "Account ban gaya! Ab login karein.")
        return redirect('login')

    return render(request, 'signup.html')


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            messages.success(request, f"Welcome {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


# Dashboard (only for logged-in users)
@login_required(login_url='login')
def dashboard_view(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, "dashboard.html", {"blogs": blogs})


# Blog detail
def blog_detail_view(request, blog_id):
    single_blog = get_object_or_404(Blog, id=blog_id)
    return render(request, "blog.html", {"blog": single_blog})


# Logout
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')


# Create blog
@login_required(login_url='login')
def create_blog_view(request):
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title or not content:
            messages.error(request, "Title aur content dono zaroori hain.")
            return render(request, 'create_blog.html')

        Blog.objects.create(
            title=title,
            content=content,
            image=image,
            author=request.user  # agar Blog me author field hai
        )

        messages.success(request, "Blog post create ho gaya!")
        return redirect('dashboard')

    return render(request, 'create_blog.html')


# Edit blog
@login_required(login_url='login')
def edit_blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)

    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title or not content:
            messages.error(request, "Title aur content dono zaroori hain.")
            return render(request, 'edit_blog.html', {"blog": blog})

        blog.title = title
        blog.content = content
        if image:
            blog.image = image
        blog.save()

        messages.success(request, "Blog post update ho gaya!")
        return redirect('dashboard')

    return render(request, 'edit_blog.html', {"blog": blog})


# Delete blog
@login_required(login_url='login')
def delete_blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    blog.delete()
    messages.success(request, "Blog post delete ho gaya!")
    return redirect('dashboard')

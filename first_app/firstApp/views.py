import random
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import OTP, Blog

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

        if not username or not password:
            messages.error(request, "Username aur password zaroori hain.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ye username already taken hai.")
            return render(request, 'signup.html')

        # Save data in the django database
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            email=email,
            password=password,
            is_active=False  # Inactive until OTP verification  
        )

        # OTP generate with random numbers
        code = str(random.randint(100000, 999999))
        OTP.objects.create(user=user, code=code)

        # Debug mode print
        if settings.DEBUG:
            print(f"DEBUG OTP for {user.username}: {code}")

        # Store in session
        request.session['otp_user_id'] = user.id

        messages.success(request, "Account ban gaya! Ab OTP verify karein.")
        return redirect('verify_otp')   # direct verify screen par bhej do

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
@login_required
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
@login_required
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
        )

        messages.success(request, "Blog post create ho gaya!")
        return redirect('dashboard')

    return render(request, 'create_blog.html')


# Edit blog
@login_required
def edit_blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

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
@login_required
def delete_blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, "Blog post delete ho gaya!")
    return redirect('dashboard')


# OTP Verification
def verify_otp_view(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "Signup pehle complete karo.")
        return redirect('signup')

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        entered = request.POST.get('otp', '').strip()

        otp = OTP.objects.filter(user=user).order_by('-created_at').first()
        if not otp:
            messages.error(request, "OTP nahi mila. Resend karen.")
            return redirect('resend_otp')

        if otp.is_expired():
            messages.error(request, "OTP expire ho gaya. Naya OTP bhej diya jayega.")
            return redirect('resend_otp')

        if otp.code == entered:
            otp.verified = True   # 🔹 FIX: OTP ko verified mark karo
            otp.save()
            user.is_active = True
            user.save()
            request.session.pop('otp_user_id', None)
            login(request, user)  # optional auto-login
            messages.success(request, "Verified — welcome!")
            return redirect('dashboard')
        else:
            otp.attempts += 1
            otp.save()
            if otp.attempts >= 5:
                messages.error(request, "Bahut wrong attempts — naya OTP bhej diya jayega.")
                return redirect('resend_otp')
            messages.error(request, "Galat OTP. Dobara try karo.")

    return render(request, 'verify_otp.html')


# Resend OTP
def resend_otp_view(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "Pehle signup karo.")
        return redirect('signup')

    user = get_object_or_404(User, id=user_id)

    # Old OTP delete ya ignore kar do
    OTP.objects.filter(user=user, verified=False).delete()

    # New OTP generate
    code = str(random.randint(100000, 999999))
    otp = OTP.objects.create(user=user, code=code)

    if settings.DEBUG:
        print(f"RESEND DEBUG OTP for {user.username}: {code}")

    messages.success(request, "Naya OTP bhej diya gaya hai.")
    return redirect('verify_otp')

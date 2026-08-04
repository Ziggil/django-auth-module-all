from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ProfileForm
from django.conf import settings
from .models import UserProfile
from django.contrib.auth import logout
from django.contrib.auth import login

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Создаем профиль
            UserProfile.objects.create(user=user)
            return redirect(getattr(settings, 'AUTH_MODULE_LOGIN_REDIRECT_URL', '/'))
    else:
        form = RegisterForm()
    return render(request, 'auth_module/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(getattr(settings, 'AUTH_MODULE_LOGIN_REDIRECT_URL', '/'))
    else:
        form = LoginForm()
    return render(request, 'auth_module/login.html', {'form': form})



from django.http import HttpResponse

def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("""
            <script>
                alert("Вы должны быть авторизированы!");
                window.location.href = '/';  // главная страница
            </script>
        """)
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        
        profile = UserProfile.objects.create(user=request.user)
    form = ProfileForm(instance=profile)
    return render(request, 'auth_module/profile.html', {'form': form})


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("""
            <script>
                alert("Вы должны быть авторизированы!");
                window.location.href = '/';  // главная страница
            </script>
        """)
    if request.method == 'POST':
        logout(request)
        return redirect(getattr(settings, 'AUTH_MODULE_LOGOUT_REDIRECT_URL', '/'))
    return render(request, 'auth_module/logout.html')
from django.contrib.auth.decorators import login_required

from .forms import MyUserRegisterForm, MyUserLoginForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import MyUser, OTP
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from .services import generate_otp_code
from django.core.mail import send_mail


def user_register(request):
    if request.method == 'POST':
        form = MyUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно создали аккаунт!')
            return redirect('index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = MyUserRegisterForm()

    return render(request, 'authentication/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = MyUserLoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_password = form.cleaned_data['password']

            user = authenticate(request, username=user_email, password=user_password)

            if user:
                if user.is_2fa_enabled:
                    otp_code = generate_otp_code()
                    OTP.objects.create(user=user, code=otp_code)
                    send_mail(subject=' Одноразовый код',
                              message= f'Ваш одноразовый пароль: {otp_code}\nНикому не показывайте!',
                              from_email=settings.DEFAULT_FROM_EMAIL,
                              recipient_list=['ayanaabdyraeva@gmail.com'],
                              fail_silently=False,
                              )
                    messages.success(request, 'Однаразовый код отправлен вам на почту.')
                    return redirect('otp_verify', user_id=user.id)
                else:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли в аккаунт!')

        messages.error(request, 'Неправильный логин или пароль')
        return redirect('index')
    else:
        form = MyUserLoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта.")
    return redirect('index')

def user_otp_verify(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)

    if request.method == 'POST':
        otp_code = request.POST['otp']

        otp = OTP.objects.filter(user=user, code=otp_code).last()

        if otp:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            otp.delete()

            return redirect('index')

        else:
            messages.error(request, 'Вы ввели неправильный код ')
    return render(request, 'authentication/otp_verify.html')

@login_required(login_url='user_login')
def user_profile(request):
    current_user = request.user
    if request.method == 'POST':
        is_2fa_enabled = 'is_2fa_enabled' in request.POST
        user = MyUser.objects.get(id=request.user.id)
        user.is_2fa_enabled = is_2fa_enabled
        user.save()

    return render(request, 'authentication/user_profile.html', {'user': current_user})


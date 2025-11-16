from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import RegisterForm, AccountsForm

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('store')  
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'accounts/signin.html')


def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        account_form = AccountsForm(request.POST, request.FILES)

        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.email 
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            account = account_form.save(commit=False)
            account.user = user
            account.save()

            messages.success(request, "Account created successfully")
            return redirect('accounts:signin')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        user_form = RegisterForm()
        account_form = AccountsForm()

    context = {'user_form': user_form, 'account_form': account_form}
    return render(request, 'accounts/register.html', context)


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('accounts:signin')

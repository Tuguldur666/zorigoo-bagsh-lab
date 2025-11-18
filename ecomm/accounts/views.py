from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import RegisterForm, AccountsForm
from accounts.models import Account

def signin(request):
    if request.method == 'POST':
        login_input = request.POST.get('identifier')   
        password = request.POST.get('password')

        user = None

        try:
            user_obj = User.objects.get(email=login_input)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user_obj = None

        if user is None:
            try:
                account_obj = Account.objects.get(phone_number=login_input)
                user = authenticate(request, username=account_obj.user.username, password=password)
            except Account.DoesNotExist:
                account_obj = None

        if user is not None:
            login(request, user)
            return redirect('store')

        messages.error(request, "Invalid email/phone or password")

    return render(request, 'accounts/signin.html')




def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        account_form = AccountsForm(request.POST, request.FILES)

        if user_form.is_valid() and account_form.is_valid():

            email = user_form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('accounts:register')

            phone_number = account_form.cleaned_data['phone_number']
            if Account.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "Phone number already exists")
                return redirect('accounts:register')

            user = user_form.save(commit=False)
            user.username = email   
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

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'account_form': account_form
    })



def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('accounts:signin')

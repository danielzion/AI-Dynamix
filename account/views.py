from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, UserLoginForm
from django.contrib.auth import login, authenticate


def register(request):
    if request.method == 'GET':
        form  = RegisterForm()
        context = {
            'form': form
            }
        return render(request, 'account/register.html', context)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            # Capitalize the first letter of the username
            username = username.capitalize()
            form.cleaned_data['username'] = username  # Update the cleaned_data
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('account:login')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {
                'form': form
                }
            return render(request, 'account/register.html', context)

    return render(request, 'account/register.html')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('/')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    # If it's a GET request or the form is invalid, render the login form
    form = UserLoginForm()  # Assuming you have a UserLoginForm defined

    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)


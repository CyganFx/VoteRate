from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = user_form.cleaned_data.get('username')
            messages.success(request, f"Account {username} has been created!")
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def index(request):
    return render(request, 'users/index.html')


@login_required
def profile(request):
    return render(request, 'users/profile.html')

from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from django.contrib import messages
import os


def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('/accounts/login/')

    else:
        f = CustomUserCreationForm()

    return render(request, os.path.join('registration', 'sign_up.html'), {'form': f})

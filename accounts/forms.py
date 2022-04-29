from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from cakeshop.models import Customer

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    phone = forms.CharField(label='Enter Phone')
    email = forms.CharField(label='Enter Elmail')
    name = forms.CharField(label='Enter name')
    address = forms.CharField(label='Enter address')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        phone = self.cleaned_data['phone']
        customer, created = Customer.objects.get_or_create(
            phonenumber=phone,
            defaults={'email': self.cleaned_data['email'],
                      'name': self.cleaned_data['name'],
                      'address': self.cleaned_data['address']}
        )

        if not created:  # Обновляем информацию о клиенте
            customer.email = self.cleaned_data['email']
            customer.name = self.cleaned_data['name']
            customer.address = self.cleaned_data['address']
            customer.save()




        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
        )

        customer.user = user
        customer.save()
        return user
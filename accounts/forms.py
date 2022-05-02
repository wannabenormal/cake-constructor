from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from cakeshop.models import Customer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import parse, is_valid_number
from phonenumbers.phonenumberutil import NumberParseException

def check_string(string, available_symbols, field, extra_symbols=[], ):
    # available_symbols is list, that can contain
    # 'en' - allow latin symbols
    # 'ru' - allow Cyrillic symbols
    # 'num' - allow numbers
    num_ascii_codes = range(48, 58)
    en_ascii_codes = list(range(65, 91)) + list(range(97, 123))
    ru_ascii_codes = range(1040, 1104)

    for symb in string:
        symb_code = ord(symb)

        if symb in extra_symbols:
            continue

        if symb_code in num_ascii_codes:
            if 'num' not in available_symbols:
                return False, f'{field} не может содержать цифры'
            continue

        elif symb_code in en_ascii_codes:
            if 'en' not in available_symbols:
                return False, f'{field} не может содержать латиницу'
            continue

        elif symb_code in ru_ascii_codes:
            if 'ru' not in available_symbols:
                return False, f'{field} не может содержать кириллицу'
            continue
        else:
            return False, f'{field} не может содержать символ "{symb}"'

    return True, 'ok'


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=18)
    phone = forms.CharField(label='Enter Phone')
    email = forms.CharField(label='Enter Email')
    name = forms.CharField(label='Enter name', max_length=25)
    address = forms.CharField(label='Enter address', max_length=100)
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Пользователь с таким именем уже существет")

        if username.isdigit():
            raise ValidationError("Имя пользователя не должно содержать только цифры")

        is_valid, error_massage = check_string(username, ['num', 'en'], 'Никнейм', ['_'])

        if not is_valid:
            raise ValidationError(error_massage)

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email)
        return email

    def clean_name(self):
        name = self.cleaned_data['name'].lower()

        is_valid, error_massage = check_string(name, ['ru', 'en'], 'Имя пользователя')

        if not is_valid:
            raise ValidationError(error_massage)

        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            parsed_phone = parse(phone)
            if not is_valid_number(parsed_phone):
                raise ValidationError('Невалидный номер телефона')
        except NumberParseException:
            raise ValidationError('Невалидный номер телефона')

        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        is_valid, error_massage = check_string(password2, ['num', 'en'], 'Пароль', ['_', '!', '@', '.', '?'])

        if not is_valid:
            raise ValidationError(error_massage)

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
import re
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Application, Review, Transport, Payment

class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=30)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)
    full_name = forms.CharField(label='ФИО', max_length=150)
    birth_date = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(label='Телефон', max_length=20)
    email = forms.EmailField(label='E-mail')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.fullmatch(r'[A-Za-z0-9]{6,}', username):
            raise forms.ValidationError('Логин: только латиница и цифры, минимум 6 символов.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже занят.')
        return username

    def clean_password(self):
        pwd = self.cleaned_data['password']
        if len(pwd) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов.')
        return pwd

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError('Пароли не совпадают.')
        return data

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(username=data['username'], password=data['password'])
        Profile.objects.create(
            user=user,
            full_name=data['full_name'],
            birth_date=data['birth_date'],
            phone=data['phone'],
            email=data['email'],
        )
        return user

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['transport', 'start_date', 'payment']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'ДД.ММ.ГГГГ'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш отзыв...'}),
        }
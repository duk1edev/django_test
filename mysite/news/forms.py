from django import forms
from .models import Category, New
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import User, UserCreationForm


class NewsForm(forms.ModelForm):
    # not conencted with model (forms.Model)
    # title = forms.CharField(max_length=100, label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # content = forms.CharField(label='Содержимое', required=True, widget=forms.Textarea(attrs={
    #     'class': 'form-control',
    #     'rows': 5,
    # }))
    # is_published = forms.BooleanField(label='Опубликовано?', initial=True)
    # category = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label='Выбирите категорию', label='Категория', widget=forms.Select(attrs={'class': 'form-control'}))

    # connected with model

    class Meta:
        model = New
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    # custom validation
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинатся с цифры')
        if len(title) < 10:
            raise ValidationError('Название должно быть больше 10 символов')
        return title

    def clean_is_published(self):
        is_published = self.cleaned_data['is_published']
        if not is_published:
            raise ValidationError("Поле 'Опубликовано' должно быть отмечено")
        return is_published


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='Имя пользователя должно быть более 150')
    email = forms.EmailField(label='Е-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # НЕ РАБОТАЕТ никто не знает
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }

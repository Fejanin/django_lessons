from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
import datetime


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин / email',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-input'
                                }))
    password = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-input'
                                }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]
        labels = {
            'email': 'Почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password1'] != cd['password2']:
    #         raise forms.ValidationError('Пароли не совпадают!')
    #     return cd['password1']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует.')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин',
                               widget=forms.TextInput())  # ...TextInput(attrs={'class': 'form-input'})
    email = forms.CharField(disabled=True, label='E-mail',
                               widget=forms.TextInput())
    this_year = datetime.date.today().year
    data_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5)))
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'photo',
            'date_birth',
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'})
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())
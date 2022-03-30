from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import django.forms as forms


class LoginForm(forms.Form):
    """
    Formularz logowania
    """
    login = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


def validate_username_is_not_taken(value):
    """
    Sprawdzenie, czy nazwa użytkownika nie jest już zajęta
    """
    if User.objects.filter(username=value):
        raise ValidationError('Ten login jest już zajęty')


class RegisterForm(forms.Form):
    """
    Formularz rejestracji
    """
    name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(label='', max_length=50, validators=[validate_username_is_not_taken],
                            widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), max_length=100)
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}),
                                max_length=100)

    def clean(self):
        """
        Sprawdzenie, czy hasła podane przy rejestracji są takie same
        """
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            raise ValidationError('Hasła nie są takie same!')
        return cleaned_data


class MyUserCreation(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name')

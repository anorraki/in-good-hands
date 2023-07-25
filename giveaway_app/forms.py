from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms


def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Hasło jest za krótkie')


def check_if_has_number(value):
    if not any(x for x in value if x.isdigit()):
        raise ValidationError('Hasło musi zawierać cyfrę')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło',
                                                                 'class': 'form-group'}),
                               validators=[validate_password, check_if_has_number],
                               help_text='Co najmniej 8 znaków')
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło',
                                                                    'class': 'form-group'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię',
                                                 'class': 'form-group'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko',
                                                'class': 'form-group'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email',
                                             'class': 'form-group'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = False
        self.fields["re_password"].label = False
        self.fields["first_name"].label = False
        self.fields["last_name"].label = False
        self.fields["email"].label = False

    def clean(self):
        data = super().clean()

        password = data.get('password')
        if password is not None and password != data.get('re_password'):
            raise ValidationError('Hasła nie są identyczne')
        return data


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-group'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło',
                                                                 'class': 'form-group'}),
                               required=False)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        widgets = {
            "password": forms.PasswordInput(attrs={'placeholder': 'Hasło'})
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = "Podaj hasło"
        self.fields["first_name"].label = "Zmień imię"
        self.fields["last_name"].label = "Zmień nazwisko"
        self.fields["email"].label = "Zmień email"


class EditPasswordForm(forms.Form):
    old_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Stare hasło'}))
    new_password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}),
                                    validators=[validate_password, check_if_has_number])
    new_password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password")
        new_password2 = cleaned_data.get("new_password_repeated")

        if new_password1 != new_password2:
            raise forms.ValidationError("Podałeś różne hasła")
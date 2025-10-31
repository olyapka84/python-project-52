from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label='First name',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        label='Last name',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'password1', 'password2')
        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Password confirmation',
        }
        help_texts = {
            'username': (
                'No more than 150 characters. '
                'Letters, digits and @/./+/-/_ characters only.'
            ),
            'password1': (
                'Password must contain at least 8 characters '
                'and not be too simple.'
            ),
            'password2': (
                'Please enter the password again for confirmation.'
            ),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

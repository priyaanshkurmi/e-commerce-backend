from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Provide clear guidance about password rules enforced by Django validators
        pw_help = (
            "Password must contain at least 8 characters, must not be a common password, "
            "and should not be too similar to your email or username."
        )
        if 'password1' in self.fields:
            self.fields['password1'].help_text = pw_help
        if 'password2' in self.fields:
            self.fields['password2'].help_text = 'Enter the same password as above for verification.'

from django import forms
from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.shortcuts import get_object_or_404
from hcaptcha.fields import hCaptchaField

from utils.validators import validate_special_char

from .models import User, Profile



class ForgetPasswordForm(forms.Form):
    email=forms.CharField(help_text="Enter your account email")
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.data.get('email')
        validate_email(email)
        return email

    # Cleaning password one to check if all validations are met
    def clean_password(self):
        ps1=self.cleaned_data.get("password")
        password_validation.validate_password(ps1,None)
        return ps1

    """Override clean on password2 level to compare similarities of password"""
    def clean_confirm_password(self):
        ps1=self.cleaned_data.get("password")
        ps2=self.cleaned_data.get("confirm_password")
        if (ps1 and ps2) and (ps1 != ps2):
            raise forms.ValidationError("The passwords does not match")
        return ps2
    
    def save(self, commit=True):
        user = get_object_or_404(User, email=self.cleaned_data.get('email'))
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    hcaptcha = hCaptchaField()

    def clean(self):
        data = super().clean()
        email = data.get('email')
        password = data.get('password')
        validate_email(email)
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError(
                    {'email': 'Please enter the correct email and password.'})
        except User.DoesNotExist:
            raise forms.ValidationError(
                {'email': 'Please enter the correct email and password.'})

        return data


class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(label="Password",
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
    )
    confirm_password=forms.CharField(widget=forms.PasswordInput(),help_text='Must be similar to first password to pass verification')

    class Meta:
        model=User
        fields=("email", "password", 'confirm_password')

    # Cleaning password one to check if all validations are met
    def clean_password(self):
        ps1=self.cleaned_data.get("password")
        password_validation.validate_password(ps1,None)
        return ps1
    
    """Override clean on password2 level to compare similarities of password"""
    def clean_confirm_password(self):
        ps1=self.cleaned_data.get("password")
        ps2=self.cleaned_data.get("confirm_password")
        if (ps1 and ps2) and (ps1 != ps2):
            raise forms.ValidationError("The passwords does not match")
        return ps2

    """ Override the default save method to use set_password method to convert text to hashed """
    def save(self, commit=True):
        user=super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password"))

        if commit:
            user.save()

        return user



class WithdrawalForm(forms.ModelForm):
    password = forms.CharField(max_length=255)

    class Meta:
        model = Profile
        fields = ('withdraw_address', 'password',)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance.user.check_password(password):
            raise forms.ValidationError('Please provide a correct password')
        return password


class ChangeEmailForm(forms.ModelForm):
    password = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'password',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.email == email:
            raise forms.ValidationError("You did not change your email")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance.check_password(password):
            raise forms.ValidationError('Please provide a correct password')
        return password

    def save(self, commit=True):
        if commit:
            self.instance.set_password(self.cleaned_data.get("password"))
            self.instance.verified = False
            self.instance.save()
        return self.instance


class ChangePasswordForm(forms.ModelForm):
    password=forms.CharField(help_text="Enter your account password")
    new_password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', 'new_password', 'confirm_password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance.check_password(password):
            raise forms.ValidationError('Please provide a correct password')
        return password

    # Cleaning password one to check if all validations are met
    def clean_new_password(self):
        ps1=self.cleaned_data.get("new_password")
        password_validation.validate_password(ps1,None)
        return ps1

    """Override clean on password2 level to compare similarities of password"""
    def clean_confirm_password(self):
        ps1=self.cleaned_data.get("new_password")
        ps2=self.cleaned_data.get("confirm_password")
        if (ps1 and ps2) and (ps1 != ps2):
            raise forms.ValidationError("The passwords does not match")
        return ps2

    def save(self, commit=True):
        self.instance.set_password(self.cleaned_data.get("new_password"))
        if commit:
            self.instance.save()
        return self.instance

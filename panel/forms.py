from decimal import Decimal
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.conf import settings
from hcaptcha.fields import hCaptchaField

from .models import Post, Message, WithdrawalRequest


class CaptchaForm(forms.Form):
    hcaptcha = hCaptchaField()


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ('title', 'slug', 'image', 'content')


class MessageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Message
        fields = ('title', 'content')


class WithdrawalForm(forms.ModelForm):

    class Meta:
        model = WithdrawalRequest
        fields = ('amount',)

    @property
    def user(self):
        return self.initial['user']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        balance = self.user.get_balance()

        if amount < settings.MIN_WITHDRAWAL:
            raise forms.ValidationError(
                f"Minimum withdrawal is {settings.MIN_WITHDRAWAL} OMI")

        if amount > float(balance):
            raise forms.ValidationError(
                f"Insufficient funds. You have {balance} OMI")

        return amount

    def save(self):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.address = self.user.profile.withdraw_address
        instance.save()
        return instance

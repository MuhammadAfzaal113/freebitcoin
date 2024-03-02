import os

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from utils.general import (convert_dollar_to_token, get_random_code,
                           parse_first_image, parse_html_text)

from .managers import TransactionManager, SurveyManager


def get_file_path(instance, filename):
    return os.path.join('blog/posts', instance.title, filename)


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to=get_file_path)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_content_text(self):
        return parse_html_text(self.content)

    def get_content_image(self):
        if not self.image:
            return parse_first_image(self.content)
        return self.image.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class RollValue(models.Model):
    lucky_number_start = models.IntegerField(default=0)
    lucky_number_end = models.IntegerField(default=10000)
    payout_dollar = models.FloatField(default=0.0)

    def get_range(self):
        return f"{self.lucky_number_start} - {self.lucky_number_end}"

    @property
    def roll_range(self):
        return self.get_range()

    @property
    def payout(self):
        return self.get_payout()

    @property
    def value_in_omi(self):
        return self.get_payount_in_token()

    def get_payout(self):
        return f"${self.payout_dollar}"

    def get_payount_in_token(self):
        calc_result = convert_dollar_to_token(self.payout_dollar)
        return '{:.8f}'.format(calc_result)

    def __str__(self):
        return self.get_range()


class Transaction(models.Model):
    TYPE = (
        ('earn', 'Earned',),
        ('referral', 'Referral Commission',),
        ('payment', 'Payment',),
    )

    tx_type = models.CharField(max_length=30, choices=TYPE)
    credit = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        'account.User', on_delete=models.DO_NOTHING, null=True)

    objects = TransactionManager()

    @property
    def transaction_type(self):
        return self.get_tx_type_display()

    def __str__(self) -> str:
        return self.get_tx_type_display()


class WithdrawalRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        'account.User', on_delete=models.DO_NOTHING)
    approved = models.BooleanField(default=False)
    address = models.CharField(max_length=100, null=True, blank=True)

    __approved = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__approved = self.approved

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.__approved is not self.approved:
            if self.approved is True:
                # Create debit transaction
                Transaction.objects.create_debit(
                    user=self.user,
                    amount=self.amount,
                )

        self.__approved = self.approved

    def __str__(self) -> str:
        return f"{self.user} - {self.amount}"

    @property
    def get_amount(self):
        return '{:.8f}'.format(self.amount)

    def get_status_html(self):
        text = "Approved" if self.approved else "Pending"
        color = "success" if self.approved else "warning"
        return mark_safe(f"<span class=\"badge bg-{color}\">{text}</span>")


class SurveyToken(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        'account.User', on_delete=models.DO_NOTHING, null=True)
    txid = models.CharField(max_length=255, blank=True, null=True)

    objects = SurveyManager()

    def __str__(self) -> str:
        return str(self.user)


class RedeemedToken(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        'account.User', on_delete=models.DO_NOTHING, null=True)

    objects = SurveyManager()

    def __str__(self) -> str:
        return str(self.user)


class PromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True, editable=False)
    valid_until = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            code = get_random_code(self)
            self.code = code

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.code


class Message(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class FreeRollLink(models.Model):
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.url


class FreeRollMembership(models.Model):
    free_roll = models.ForeignKey(FreeRollLink, on_delete=models.CASCADE)
    user = models.ForeignKey(
        'account.User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def use_link(self):
        self.created = timezone.now()

    def is_active(self):
        return (timezone.now() - self.created) > timezone.timedelta(
            seconds=settings.ROLL_LINK_LIFETIME)

    def __str__(self) -> str:
        return f"{self.free_roll} - {self.user}"


@receiver(post_save, sender=Transaction)
def save_profile(sender, created, instance, **kwargs):
    if created:
        ref = instance.user.profile.referrer
        if ref:
            bonus = float(instance.amount) * 0.5
            Transaction.objects.create(
                tx_type='referral',
                credit=True,
                amount=bonus,
                user=ref
            )

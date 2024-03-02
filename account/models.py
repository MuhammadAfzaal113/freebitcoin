import uuid
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from utils.general import convert_dollar_to_token

from utils.general import get_random_code, send_email

from .utils import get_name_from_email


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None,
        is_active=True, is_staff=False, is_admin=False
    ):
        if not email:
            raise ValueError("User must provide an email")
        if not password:
            raise ValueError("User must provide a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user

    def create_staff(self, email, password=None):
        user = self.create_user(email=email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email, password=password, is_staff=True, is_admin=True)
        return user

    def get_staffs(self):
        return self.filter(staff=True)

    def get_admins(self):
        return self.filter(admin=True)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)

    verified = models.BooleanField(default=False)

    # Admin fields
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def username(self):
        return self.profile.username

    @property
    def get_emailname(self):
        # Return the x part of an email e.g [x]@gmail.com
        return self.email.split('@')[0]

    def __str__(self):
        return self.email

    def email_user(self, subject, message):
        val = send_email(subject=subject, message=message, email=self.email)
        return True if val else False

    def count_referrals(self):
        return Profile.objects.filter(referrer=self).count()

    def get_link_memberships(self):
        return self.freerollmembership_set.all()

    def get_roll_link_membership(self, link):
        link_membership = self.get_link_memberships().filter(
            free_roll=link).first()
        return link_membership

    def can_use_roll_link(self, link):
        link_membership = self.get_roll_link_membership(link)
        if link_membership:
            return link_membership.is_active()
        return True

    def use_roll_link(self, link):
        self.profile.reset_roll_time()
        link_membership = self.get_roll_link_membership(link)
        if link_membership:
            link_membership.use_link()
            link_membership.save()
            return
        self.freerollmembership_set.create(free_roll=link)

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def is_superuser(self):
        return self.is_admin()

    def get_balance(self):
        balance = self.transaction_set.get_credits().sum_amount()
        debited = self.transaction_set.get_debits().sum_amount()
        balance = balance - debited
        return '{:.4f}'.format(balance)

    def get_token_balance(self):
        """Get token balance"""
        token_total = self.surveytoken_set.sum_amount()
        redeemed_total = self.redeemedtoken_set.sum_amount()
        balance = token_total - redeemed_total
        return '{:.4f}'.format(balance)

    def total_earned_referral(self):
        total = self.transaction_set.total_earned_referral()
        return '{:.8f}'.format(total)

    def recent_earned_referral(self):
        total = self.transaction_set.recent_earned_referral()
        return '{:.8f}'.format(total)

    @cached_property
    def token_balance(self):
        return self.get_token_balance()

    @cached_property
    def token_balance_text(self):
        return f"{float(self.token_balance):,}"

    @cached_property
    def token_balance_in_omi(self):
        in_usd = float(self.token_balance) / settings.TOKEN_PER_USD
        in_omi = convert_dollar_to_token(in_usd)
        decimal_limit_format = f"{in_omi:.8f}"
        top, bottom = decimal_limit_format.split('.')
        comma_format = f"{int(top):,}"
        bottom = bottom if bottom else "0"
        return f"{comma_format}.{bottom}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=60, unique=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(
        blank=True, null=True, max_length=10, help_text='Referral id')

    # Referrer
    referrer = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True, related_name='referrer_set')

    roll_time = models.IntegerField(default=0)
    withdraw_address = models.CharField(max_length=255, blank=True)

    promo_codes = models.ManyToManyField('panel.PromoCode')

    def has_used_promo_code(self, code):
        return self.promo_codes.filter(code=code).exists()

    def reset_roll_time(self):
        self.roll_time = self.roll_time - settings.ROLL_SECONDS
        self.save()

    def use_promo_code(self, code):
        self.reset_roll_time()
        self.promo_codes.add(code)

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate new referral id
            self.code = get_random_code(self)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.get_or_create(
                user=instance, username=get_name_from_email(instance.email))
        except Exception as e:
            instance.delete()
            raise e

from account.models import Profile
from django.conf import settings
from django.db import transaction
from django.db.models import Manager, QuerySet, Sum
from django.utils.timezone import timedelta
from django.utils import timezone

from utils.general import convert_dollar_to_token


class TransactionQuery(QuerySet):
    def sum_amount(self):
        value = self.aggregate(Sum('amount'))['amount__sum']
        return value or 0

    def date_sum_amount(self, date):
        addition = timedelta(days=1)
        return self.filter(
                created__gte=date
            ).filter(
                created__lt=(date + addition)
            ).sum_amount()

    def get_credits(self):
        return self.filter(credit=True)

    def get_debits(self):
        return self.filter(credit=False)

    def get_earned(self):
        return self.get_credits().filter(tx_type="earn")

    def get_payments(self):
        return self.get_credits().filter(tx_type="payment")

    def get_referrals(self):
        return self.get_credits().filter(tx_type="referral")

    def total_earned_referral(self):
        return self.get_referrals().sum_amount()

    def recent_earned_referral(self):
        return self.get_referrals().date_sum_amount(
            timezone.now() - timedelta(days=1))


class TransactionManager(Manager):
    def get_queryset(self):
        return TransactionQuery(self.model, using=self._db)

    def sum_amount(self):
        return self.get_queryset().sum_amount()

    def date_sum_amount(self, date):
        return self.get_queryset().date_sum_amount(date)

    def get_credits(self):
        return self.get_queryset().get_credits()

    def get_debits(self):
        return self.get_queryset().get_debits()

    def get_earned(self):
        return self.get_queryset().get_earned()

    def get_payments(self):
        return self.get_queryset().get_payments()

    def get_referrals(self):
        return self.get_queryset().get_referrals()

    def total_earned_referral(self):
        return self.get_queryset().total_earned_referral()

    def recent_earned_referral(self):
        return self.get_queryset().recent_earned_referral()

    def add_survey_transaction(self, user, amount):
        """Create new redeemed transaction"""
        return self.create(
            user=user,
            amount=amount,
            credit=True,
            tx_type="earn",
        )

    def create_debit(self, user, amount):
        """Create debit transaction"""
        return self.create(
            user=user,
            amount=amount,
            credit=False,
            tx_type="payment",
        )


class SurveyQuery(QuerySet):
    def sum_amount(self):
        value = self.aggregate(Sum('amount'))['amount__sum']
        return value or 0


class SurveyManager(Manager):
    def get_queryset(self):
        return SurveyQuery(self.model, using=self._db)

    def sum_amount(self):
        return self.get_queryset().sum_amount()

    def add_survey_transaction(self, uid, amount, txid):
        """Create new survey token"""
        if not self.filter(txid=txid).exists():
            user = Profile.objects.get(uid=uid).user
            return self.create(
                user=user,
                amount=amount,
                txid=txid
            )

    @transaction.atomic
    def redeem_tokens(self, user, amount):
        """Redeem tokens to transactions"""
        token_balance = float(user.get_token_balance())

        if token_balance < amount:
            raise ValueError('You do not have enough tokens')

        # Convert tokens to dollars then to omi
        amount_in_dollars = amount / settings.TOKEN_PER_USD
        amount_in_omi = convert_dollar_to_token(amount_in_dollars)

        # add to transactions of omi
        user.transaction_set.add_survey_transaction(
            user, amount_in_omi
        )

        # Add to redeemed tokens
        user.redeemedtoken_set.create(
            user=user,
            amount=amount
        )


class RedeemedTokenQuery(QuerySet):
    def sum_amount(self):
        value = self.aggregate(Sum('amount'))['amount__sum']
        return value or 0


class RedeemedTokenManager(Manager):
    def get_queryset(self):
        return RedeemedTokenQuery(self.model, using=self._db)

    def sum_amount(self):
        return self.get_queryset().sum_amount()

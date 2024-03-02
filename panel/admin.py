from django.contrib import admin

from .forms import MessageAdminForm, PostAdminForm
from .models import (FreeRollLink, FreeRollMembership, Message, Post,
                     PromoCode, RollValue, Transaction, SurveyToken, RedeemedToken, WithdrawalRequest)


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {
        'slug': ['title'],
    }


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'created',)
    list_filter = ('tx_type', 'credit', 'created',)


class RollValueAdmin(admin.ModelAdmin):
    list_display = ('roll_range', 'payout', 'value_in_omi')


class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm


admin.site.register([PromoCode, FreeRollLink, FreeRollMembership, SurveyToken, RedeemedToken, WithdrawalRequest])
admin.site.register(Post, PostAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(RollValue, RollValueAdmin)
admin.site.register(Transaction, TransactionAdmin)

from django.urls import path

from . import views


app_name = 'panel'
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("use-promo-code/", views.view_use_promo_code, name="use_promo_code"),
    path("withdrawals/", views.Withdraw.as_view(), name="withdrawal"),
    path("statistics/", views.Stats.as_view(), name="stats"),
    path("referral/", views.Referral.as_view(), name="referral"),
    path("free-rolls/", views.FreeRollsView.as_view(), name="free_rolls"),
    path(
        "free-rolls/use-link/<int:link_id>/",
        views.use_free_roll_link, name="use_free_rolls"),

    path("messages/", views.Messages.as_view(), name="messages"),
    path(
        "message/detail/<str:slug>/",
        views.MessageDetail.as_view(), name="message-detail"),
    path("earn-more/", views.EarnMorePage.as_view(), name="earn_more"),
    path("redeem/", views.redeem_tokens, name="redeem"),
]

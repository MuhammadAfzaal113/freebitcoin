from django.urls import path

from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.login_account, name='login'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('register/', views.register_account, name='register'),
    path('logout/', views.Logout, name='logout'),

    path(
        "activate/<slug:uidb64>/<slug:token>/",
        views.activate_email, name="activate"),
    path(
        'resend_activation_link/',
        views.resend_activation_link, name='resend_activation_link'),
    path('settings/', views.Settings.as_view(), name='settings'),
    path('export/', views.export, name='export'),
]

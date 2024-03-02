from django.urls import path

from . import views


app_name = 'landing'
urlpatterns = [
    path("", views.Index.as_view(), name="landing"),
    path("faq/", views.Faq.as_view(), name="faq"),
    path("gdpr/", views.GDPR.as_view(), name="gdpr"),
    path("blog/", views.Blog.as_view(), name="blog"),
    path(
        "blog/post/<str:slug>/",
        views.BlogDetailPage.as_view(), name="blog-post"),

    # Callable for receiving bitlab request
    path("bitlab/", views.bitlab_callback, name="bitlab-callback"),

    # Callable for receiving cpx request
    path("cpx/", views.cpx_callback, name="cpx-callback"),
]

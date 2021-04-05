from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from . import views
from .forms import AccountLoginForm, PwdResetConfirmForm, PwdResetForm

app_name = "account"

urlpatterns = [
    path("register/", views.account_register, name="register"),
    path("activate/<slug:uidb64>/<slug:token>/", views.account_activate, name="activate"),
    # Login/Logout
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="account/registration/login.html",
            redirect_authenticated_user=True,
            form_class=AccountLoginForm,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="account:login"), name="logout"),
    # Reset password
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password/password_reset_form.html",
            email_template_name="account/password/password_reset_email.html",
            success_url=reverse_lazy("account:password_reset_done"),
            form_class=PwdResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(template_name="account/password/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password_reset_confirm.html",
            success_url=reverse_lazy("account:password_reset_complete"),
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    # User dashboard
    path("dashboard/", views.account_dashboard, name="dashboard"),
    path("profile/edit/", views.account_edit, name="edit"),
    path("profile/delete/", views.account_delete, name="delete"),
    path(
        "profile/delete-confirm/",
        TemplateView.as_view(template_name="account/user/delete_confirm.html"),
        name="delete_confirm",
    ),
]

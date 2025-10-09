from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"),  name='login'),
    path("reset/", auth_views.PasswordResetView.as_view(template_name="registration/passwordreset.html", html_email_template_name='registration/password_reset_email.html'),  name='password_reset'),
    path("reset_enviado/", auth_views.PasswordResetDoneView.as_view(),  name='password_reset_done'),
    path("reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(),  name='password_reset_confirm'),
    path("reset_completo/", auth_views.PasswordResetCompleteView.as_view(),  name='password_reset_complete'),
    path("logout/", auth_views.LogoutView.as_view(),  name='logout'),
]
from django.urls import path
from django.contrib.auth import views as auth_views
from reset import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name='reset/login.html', redirect_authenticated_user=True),
         name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name='reset/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(
        template_name ='reset/password_reset_done.html'), name="password_reset_done"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name='reset/password_reset_complete.html'), name="password_reset_complete"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="reset/password_reset.html"),
         name="passwordreset"),

]
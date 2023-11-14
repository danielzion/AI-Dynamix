from django.urls import path
from . import views
from .forms import UserLoginForm

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, LogoutView

app_name = 'account'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),  
    path('logout', LogoutView.as_view(next_page='home'), name='logout'),
    path('password_change/done', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'),
    path('password_change', PasswordChangeView.as_view(template_name='accounts/password_change_form.html'),
        name='password_change'),
    path('password_reset/done', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('password_reset', PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
        name='password_reset'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
]


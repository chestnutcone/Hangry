from django.urls import path, reverse_lazy, reverse
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url="/users/password_reset/done/"),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(success_url="/users/reset/done/"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

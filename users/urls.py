from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.RegistrationCreateView.as_view(), name='registration'),
    path('profile/', login_required(views.ProfileUpdateView.as_view()), name='profile'),
    path('logout/', views.logout, name='logout'),
    path('email_verification/<str:email>/<uuid:code>/', views.EmailVerificationView.as_view(), name='email_verification'),
]

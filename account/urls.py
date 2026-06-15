from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    #path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.UserRegistrationView.as_view(template_name = "account/registration/register.html"), name='UserRegistrationView'),
    path('login/', views.LoginView.as_view(template_name = "account/registration/login.html"), name='login'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'volunteers'
urlpatterns = [
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail_view'),
    path('profile/', views.ProfileView.as_view(), name='profile_view'),
    
]
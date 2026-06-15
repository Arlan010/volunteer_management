from django.urls import path
from . import views
app_name = 'volunteers'
urlpatterns = [
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail_view'),
    path('profile/', views.ProfileView.as_view(), name='profile_view'),
    
]

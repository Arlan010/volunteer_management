from django.urls import path
from . import views
app_name = 'organization'
urlpatterns = [
    path('projects/', views.ProjectListView.as_view(), name='project_view'),
    path('projects/create/<int:pk>/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('add/', views.OrganizationCreateView.as_view(), name='organization_create_view'),
    path('response/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail_view'),
    path('profile/', views.ProfileView.as_view(), name='profile_view'),
    path('profile/update/<int:pk>', views.UpdateProfileView.as_view(), name='update_profile_view'),
    path('projects/map', views.project_view_map, name='projects'),
]

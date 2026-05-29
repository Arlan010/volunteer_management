from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'main'
urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('category/<int:category_id>', views.MainCategory.as_view(), name='category'),
    path('project/list/', views.project_list, name='project_list'),
    path('news/list/', views.news_list, name='news_list'),
    path('notification/<int:id>', views.notification_list, name='notification_list'),
]
from django.urls import path
from . import views
app_name = 'news'
urlpatterns = [
    path('detail/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
]

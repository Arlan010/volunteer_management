from django.shortcuts import render
from  django.views.generic import ListView,DetailView,CreateView
from .models import News
# Create your views here.

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

class NewsSidebarView(ListView):
    models = News
    template_name = 'news/news_sidebar.html'
    context_object_name = "my_news"

    def get_queryset(self):
        return News.objects.all().order_by('-created_date')[:3]

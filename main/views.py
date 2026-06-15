from django.shortcuts import render,redirect
from organization.models import Project,Category
from django.views.generic.base import TemplateView,View
from news.models import News
from .forms import SupportForm
from account.models import CustomUser
from .models import Support
from django.contrib import messages

class MainView(TemplateView,View):
    template_name = 'main/index.html'
    def get(self,request,category_id = None):
        form = SupportForm()
        projects = Project.objects.all()[:4]
        categorys = Category.objects.all()
        my_news = News.objects.all()[:3]
        if category_id:
            print(category_id)
            projects = Project.objects.filter(category=category_id)
        return self.render_to_response({'projects':projects,'categorys':categorys,'my_news':my_news,'form':form})

    def post(self, request,category_id = None):
        user = CustomUser.objects.get(id = request.user.id)
        print(user.id)
        form = SupportForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.user
            form.save()
            messages.success(request, "You have been sent successfully" )
            return redirect('main:main')
        return self.render_to_response({'projects':projects,'categorys':categorys,'my_news':my_news,'form':form})

class MainCategory(TemplateView,View):
    template_name = 'main/index.html'
    def get(self,request,category_id ):
        form = SupportForm()
        projects = Project.objects.filter(category=category_id)
        categorys = Category.objects.all()
        my_news = News.objects.all()[:3]
        return self.render_to_response({'projects':projects,'categorys':categorys,'my_news':my_news,'form':form})

    def post(self, request,category_id):
        user = CustomUser.objects.get(id = request.user.id)
        print(user.id)
        form = SupportForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.user
            form.save()
            messages.success(request, "You have been sent successfully" )
            return redirect('main:main')
        return self.render_to_response({'projects':projects,'categorys':categorys,'my_news':my_news,'form':form})
        
def project_list(request):
	projects = Project.objects.all()

	return render(request, 'main/project_list.html', {'projects':projects})

def news_list(request):
	my_news = News.objects.all()

	return render(request, 'main/news_list.html', {'my_news':my_news})

def notification_list(request, id):
    user = CustomUser.objects.get(id = id)
    print(user)
    support = Support.objects.filter(user_id = user)
    return render(request, 'main/notification.html', {'support':support})

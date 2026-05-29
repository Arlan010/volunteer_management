from django.shortcuts import render
from  django.views.generic import ListView,DetailView,CreateView
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,View
from organization.models import Project,ResponseProject
from account.models import CustomUser

class ProjectDetailView(TemplateView,View):
    template_name = 'volunteers/project_detail.html'

    def get(self,request,pk):
        projects_details = Project.objects.get(id=pk)
        
        return self.render_to_response({'projects_details':projects_details})

    def post(self, request,pk):
        if request.POST:
            user_id = request.POST.get("user_id")
            user = CustomUser.objects.get(id = user_id)
            projects_details = Project.objects.get(id=pk)
            response_project = ResponseProject(user_id=user, project=projects_details)
            response_project.save()
            return redirect('volunteers:project_detail_view' ,pk=pk)

class ProfileView(TemplateView):
    template_name = 'volunteers/profile.html'

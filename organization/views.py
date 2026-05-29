from django.shortcuts import render,redirect
from .models import Organization,Project,ResponseProject
from account.models import CustomUser
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from  django.views.generic import ListView,DetailView,CreateView
from django.views.generic.base import TemplateView,View
from django.db.models import F
from .forms import ProjectForm,OrganizationForm,UserEditForm

class ProfileView(TemplateView):
    template_name = 'organization/profille.html'

class ProjectListView(ListView):
    models = Project
    template_name = 'organization/index.html'
    context_object_name = "projects"
    def get_queryset(self):
        return Project.objects.filter(organization_id=self.request.user.organization.id)

class ProjectCreateView(CreateView):
    template_name = 'organization/project_create.html'
    form_class = ProjectForm
    
    def post(self, request, *args,**kwargs):
        pk = self.kwargs.get('pk')
        organization = Organization.objects.get(id = pk)
        form = self.form_class(request.POST, files=request.FILES)
        if form.is_valid():
            new_form =form.save(commit=False)
            new_form.organization_id = organization
            form.save()
            return redirect('organization:project_view')
        return self.render_to_response({'form_class': form_class})

class ProjectDetailView(TemplateView):
    template_name = 'organization/projects_detail.html'

    def get(self,request,pk):
        projects_details = Project.objects.get(id = pk)
        response_projects = ResponseProject.objects.filter(project = projects_details)
        return self.render_to_response({'projects_details':projects_details,'response_projects':response_projects})

    def post(self, request,pk):
        projects_details = Project.objects.get(id = pk)
        if request.method == 'POST':
            button = request.POST['button']
            if button == 'the volunteer did not come':
                print(True)
                volunteer_id = request.POST.get("volunteer_id")
                CustomUser.objects.filter(id = volunteer_id).update(rating = F("rating") - 10)
                return redirect('organization:project_detail_view', pk=projects_details.id)
            else:
                rating = request.POST.get("rating")
                volunteer_id = request.POST.get("volunteer_id")
                CustomUser.objects.filter(id = volunteer_id).update(rating = F("rating") +rating)
                return redirect('organization:project_detail_view', pk=projects_details.id)
            

class OrganizationCreateView(TemplateView,View):
    template_name = 'organization/create.html'

    def get(self,request):
        form = OrganizationForm()
        return self.render_to_response({'form':form})

    def post(self, request):
        user = CustomUser.objects.get(id = request.user.id)
        print(user)
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = user
            form.save()
            return redirect('organization:project_view')

class UpdateProfileView(TemplateView,View):
    template_name = 'organization/update_profille.html'
    def get(self,request,pk):
        form = OrganizationForm(instance=request.user.organization)
        user_form = UserEditForm(instance=request.user)
        return self.render_to_response({'form':form,'user_form':user_form})

    def post(self, request,pk):
        if request.method == 'POST':
            user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
            form = OrganizationForm(
                                    instance=request.user.organization,
                                    data=request.POST)
            if user_form.is_valid() and form.is_valid():
                user_form.save()
                form.save()
                return redirect('organization:profile_view')
            else:
                user_form = UserEditForm(instance=request.user)
                form = OrganizationForm(instance=request.user.organization)


from django.http import JsonResponse
from .models import VolunteerProject
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def project_view_map(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        project = VolunteerProject.objects.create(
            title=data['title'],
            description=data['description'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            start_date=data['start_date'],
            status=data['status']
        )
        return JsonResponse({'id': project.id}, status=201)

    elif request.method == 'GET':
        projects = list(VolunteerProject.objects.filter(status='current').values())
        return render(request, 'main/projects_map.html', {'projects': projects})
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse, reverse_lazy
from .models import Organization,Project,ResponseProject
from account.models import CustomUser
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.views.generic.base import TemplateView,View
from django.db.models import Sum
from .forms import ProjectForm,OrganizationForm,UserEditForm
from account.mixins import OrganizationRequiredMixin

class ProfileView(OrganizationRequiredMixin, TemplateView):
    template_name = 'organization/profille.html'

class ProjectListView(OrganizationRequiredMixin, ListView):
    model = Project
    template_name = 'organization/index.html'
    context_object_name = "projects"
    def get_queryset(self):
        return Project.objects.filter(organization=self.request.user.organization)

class ProjectCreateView(OrganizationRequiredMixin, CreateView):
    template_name = 'organization/project_create.html'
    form_class = ProjectForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_organization:
            pk = self.kwargs.get('pk')
            if pk and pk != request.user.organization.id:
                raise PermissionDenied("Бұл ұйым үшін жоба қосуға рұқсат жоқ.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        form.save()
        return redirect('organization:project_view')

class ProjectUpdateView(OrganizationRequiredMixin, UpdateView):
    template_name = 'organization/project_create.html'
    form_class = ProjectForm

    def get_queryset(self):
        return Project.objects.filter(organization=self.request.user.organization)

    def get_success_url(self):
        return reverse('organization:project_detail_view', kwargs={'pk': self.object.id})

class ProjectDeleteView(OrganizationRequiredMixin, DeleteView):
    model = Project

    def get_queryset(self):
        return Project.objects.filter(organization=self.request.user.organization)

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        return redirect('organization:project_detail_view', pk=project.id)

    def get_success_url(self):
        return reverse_lazy('organization:project_view')

def recalculate_user_rating(user_id):
    total_rating = ResponseProject.objects.filter(user_id=user_id).aggregate(
        total=Sum('rating')
    )['total'] or 0
    CustomUser.objects.filter(id=user_id).update(rating=total_rating)


class ProjectDetailView(OrganizationRequiredMixin, TemplateView):
    template_name = 'organization/projects_detail.html'

    def get(self,request,pk):
        projects_details = get_object_or_404(Project, id=pk, organization=request.user.organization)
        response_projects = ResponseProject.objects.filter(project=projects_details).select_related('user')
        return self.render_to_response({'projects_details':projects_details,'response_projects':response_projects})

    def post(self, request,pk):
        projects_details = get_object_or_404(Project, id=pk, organization=request.user.organization)
        if request.method == 'POST':
            volunteer_id = request.POST.get("volunteer_id")
            response_project = get_object_or_404(
                ResponseProject,
                project=projects_details,
                user_id=volunteer_id,
            )

            if request.POST.get('action') == 'missed':
                response_project.rating = -2
            else:
                rating = request.POST.get("rating") or 0
                response_project.rating = int(rating)

            response_project.save(update_fields=['rating'])
            recalculate_user_rating(volunteer_id)
            return redirect('organization:project_detail_view', pk=projects_details.id)
            

class OrganizationCreateView(OrganizationRequiredMixin, TemplateView,View):
    template_name = 'organization/create.html'

    def get(self,request):
        if Organization.objects.filter(user=request.user).exists():
            return redirect('organization:profile_view')
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

class UpdateProfileView(OrganizationRequiredMixin, TemplateView,View):
    template_name = 'organization/update_profille.html'
    def get(self,request,pk):
        if pk != request.user.id:
            raise PermissionDenied("Өзге пайдаланушының профилін өңдеуге рұқсат жоқ.")
        form = OrganizationForm(instance=request.user.organization)
        user_form = UserEditForm(instance=request.user)
        return self.render_to_response({'form':form,'user_form':user_form})

    def post(self, request,pk):
        if pk != request.user.id:
            raise PermissionDenied("Өзге пайдаланушының профилін өңдеуге рұқсат жоқ.")
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


def project_view_map(request):
    projects = Project.objects.filter(
        status='current',
        latitude__isnull=False,
        longitude__isnull=False,
    )
    return render(request, 'main/projects_map.html', {'projects': projects})

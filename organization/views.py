from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse, reverse_lazy
from .models import Organization,Project,ResponseProject
from account.models import CustomUser, Notification
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
        projects_details = get_object_or_404(Project.objects.select_related('organization'), id=pk, organization=request.user.organization)
        response_projects = ResponseProject.objects.filter(project=projects_details).select_related('user').order_by('-created_date')
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

            attendance_status = request.POST.get('attendance_status') or ResponseProject.ATTENDANCE_PENDING
            if attendance_status not in dict(ResponseProject.ATTENDANCE_CHOICES):
                attendance_status = ResponseProject.ATTENDANCE_PENDING

            if attendance_status == ResponseProject.ATTENDANCE_MISSED:
                response_project.rating = -2
            elif attendance_status == ResponseProject.ATTENDANCE_ATTENDED:
                try:
                    rating = int(request.POST.get("rating") or 0)
                except (TypeError, ValueError):
                    rating = 0
                response_project.rating = max(0, min(5, rating))
            else:
                response_project.rating = 0

            response_project.attendance_status = attendance_status
            response_project.save(update_fields=['rating', 'attendance_status'])
            recalculate_user_rating(volunteer_id)
            status_label = dict(ResponseProject.ATTENDANCE_CHOICES).get(attendance_status, attendance_status)
            Notification.objects.create(
                recipient=response_project.user,
                title='Жоба бойынша жаңарту',
                message=f'"{projects_details.title}" жобасында статусыңыз жаңартылды: {status_label}. Рейтинг: {max(response_project.rating, 0)}.',
                url=reverse('volunteers:project_detail_view', kwargs={'pk': projects_details.id}),
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'attendance_status': response_project.attendance_status,
                    'rating': max(response_project.rating, 0),
                })
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
                                 data=request.POST,
                                 files=request.FILES)
            form = OrganizationForm(
                                    instance=request.user.organization,
                                    data=request.POST)
            if user_form.is_valid() and form.is_valid():
                user_form.save()
                form.save()
                return redirect('organization:profile_view')
            return self.render_to_response({'form': form, 'user_form': user_form})


def project_view_map(request):
    projects = Project.objects.filter(
        status='current',
        latitude__isnull=False,
        longitude__isnull=False,
    )
    project_markers = [
        {
            'title': project.title,
            'location': project.location,
            'comment': project.comment,
            'latitude': project.latitude,
            'longitude': project.longitude,
            'start_date': project.start_date.strftime('%d.%m.%Y') if project.start_date else '',
        }
        for project in projects
    ]
    return render(request, 'main/projects_map.html', {'project_markers': project_markers})

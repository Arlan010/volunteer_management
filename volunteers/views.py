from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView,View
from account.models import Notification
from organization.models import Project,ResponseProject
from account.mixins import VolunteerRequiredMixin
from .forms import VolunteerProfileForm

class ProjectDetailView(TemplateView,View):
    template_name = 'volunteers/project_detail.html'

    def get(self,request,pk):
        projects_details = get_object_or_404(Project.objects.select_related('organization__user'), id=pk)
        user_has_responded = False
        is_author_organization = False
        is_other_organization = False
        response_projects = ResponseProject.objects.none()

        if request.user.is_authenticated:
            if request.user.is_volunteer:
                user_has_responded = ResponseProject.objects.filter(
                    user=request.user,
                    project=projects_details,
                ).exists()
            elif request.user.is_organization:
                is_author_organization = (
                    hasattr(request.user, 'organization')
                    and projects_details.organization_id == request.user.organization.id
                )
                is_other_organization = not is_author_organization
                if is_author_organization:
                    response_projects = ResponseProject.objects.filter(
                        project=projects_details,
                    ).select_related('user').order_by('-created_date')

        return self.render_to_response({
            'projects_details': projects_details,
            'user_has_responded': user_has_responded,
            'is_author_organization': is_author_organization,
            'is_other_organization': is_other_organization,
            'response_projects': response_projects,
        })

    def post(self, request,pk):
        if not request.user.is_authenticated:
            return redirect('account:login')
        if not request.user.is_volunteer:
            raise PermissionDenied("Жобаға тек волонтерлер қосыла алады.")
        if request.POST:
            user = request.user
            projects_details = get_object_or_404(Project.objects.select_related('organization__user'), id=pk)
            _, created = ResponseProject.objects.get_or_create(user=user, project=projects_details)
            if created:
                Notification.objects.create(
                    recipient=projects_details.organization.user,
                    title='Жобаға жаңа өтінім',
                    message=f'{user.first_name or user.username} "{projects_details.title}" жобасына қосылуға өтінім берді.',
                    url=reverse('organization:project_detail_view', kwargs={'pk': projects_details.id}),
                )
            return redirect('volunteers:project_detail_view' ,pk=pk)

class ProfileView(VolunteerRequiredMixin, TemplateView):
    template_name = 'volunteers/profile.html'


class UpdateProfileView(VolunteerRequiredMixin, TemplateView, View):
    template_name = 'volunteers/update_profile.html'

    def get(self, request):
        form = VolunteerProfileForm(instance=request.user)
        return self.render_to_response({'form': form})

    def post(self, request):
        form = VolunteerProfileForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            form.save()
            return redirect('volunteers:profile_view')
        return self.render_to_response({'form': form})

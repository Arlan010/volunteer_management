from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView,View
from organization.models import Project,ResponseProject
from account.mixins import VolunteerRequiredMixin

class ProjectDetailView(TemplateView,View):
    template_name = 'volunteers/project_detail.html'

    def get(self,request,pk):
        projects_details = get_object_or_404(Project.objects.select_related('organization'), id=pk)
        user_has_responded = False
        is_author_organization = False
        is_other_organization = False

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

        return self.render_to_response({
            'projects_details': projects_details,
            'user_has_responded': user_has_responded,
            'is_author_organization': is_author_organization,
            'is_other_organization': is_other_organization,
        })

    def post(self, request,pk):
        if not request.user.is_authenticated:
            return redirect('account:login')
        if not request.user.is_volunteer:
            raise PermissionDenied("Жобаға тек волонтерлер қосыла алады.")
        if request.POST:
            user = request.user
            projects_details = get_object_or_404(Project, id=pk)
            ResponseProject.objects.get_or_create(user=user, project=projects_details)
            return redirect('volunteers:project_detail_view' ,pk=pk)

class ProfileView(VolunteerRequiredMixin, TemplateView):
    template_name = 'volunteers/profile.html'

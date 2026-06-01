from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class VolunteerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Allow only authenticated volunteers."""
    login_url = 'account:login'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_volunteer

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("Бұл бетке тек волонтерлер кіре алады.")


class OrganizationRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Allow only authenticated organizations."""
    login_url = 'account:login'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_organization

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("Бұл бетке тек ұйымдар кіре алады.")

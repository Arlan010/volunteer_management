from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin,View
from .forms import UserRegistrationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.urls import reverse_lazy


class LoginView(auth_views.LoginView):
    def get_success_url(self):  #Определите URL-адрес для перенаправления после успешной проверки формы. 
                                #Возвращает success_urlпо умолчанию.
        if self.request.user.role == 1:
            return reverse_lazy('main:main')
        elif self.request.user.role == 2:
            return reverse_lazy('organization:profile_view')


def logout_view(request):
    logout(request)
    return redirect('main:main')
    
        
class UserRegistrationView(TemplateResponseMixin, View):
    template_name = 'registration/registration.html'

    def get(self,request):
        registration_form = UserRegistrationForm()
        return self.render_to_response({'registration_form': registration_form})

    def post(self, request):
        registration_form = UserRegistrationForm(request.POST, files=request.FILES)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
        # Set the chosen password
            new_user.set_password(
            registration_form.cleaned_data['password'])
        # Save the User object
            new_user.save()
            return redirect('account:login')
        return self.render_to_response({'registration_form': registration_form})


class NotificationListView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'account/notifications.html'
    login_url = 'account:login'

    def get(self, request):
        notifications = request.user.notifications.all()
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return self.render_to_response({'notifications': notifications})

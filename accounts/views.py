from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from accounts.forms import RegistrationForm, UserAuthenticationForm
from accounts.models import User
from django.urls import reverse_lazy


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "accounts/customer-registration.html"
    form_class = RegistrationForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('accounts:login')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/customer-login.html'
    authentication_form = UserAuthenticationForm
    next_page = None
    redirect_authenticated_user = None
    success_message = "You've logged in successfully."

    def get_success_url(self):
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            name = self.request.user.get_type_display().lower()
            self.next_page = reverse_lazy(f"{name}:index")
        return self.next_page

    def dispatch(self, request, *args, **kwargs):
        self.redirect_authenticated_user = True
        if self.request.user.is_authenticated and self.request.user.is_staff:
            self.redirect_authenticated_user = False
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        name = self.request.user.get_type_display().lower()
        self.next_page = f"{name}:index"
        return super(UserLoginView, self).form_valid(form)


class LogoutView(View):

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, "You've logged out successfully.")
        return redirect('accounts:login')

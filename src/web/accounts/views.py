from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.contrib.auth import logout, authenticate
from src.web.accounts.forms import UserProfileForm, PasswordForm


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('account_login')


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):
    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('account_login')

        if request.user.is_staff:
            return redirect('admins:dashboard')

        if request.user.is_superuser:
            return redirect('/admin/')

        return redirect('/')



class UserAccountBaseView(View):
    """ Base view for account actions like deactivation and deletion """
    form_class = PasswordForm
    template_name = None
    success_message = None
    success_url = None

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def perform_action(self, user):
        """ Override this method in child views to perform specific actions (deactivate/delete) """
        raise NotImplementedError("Subclasses must implement perform_action method.")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Validate the password
            user = authenticate(email=email, password=password)
            if user is None:
                messages.error(request, 'Enter a valid Email or Password')
                return render(request, self.template_name, {'form': form})

            # Perform the specific action (deactivate or delete)
            self.perform_action(user)

            messages.success(request, self.success_message)
            return redirect(self.success_url)  # Redirect to success page after action

        return render(request, self.template_name, {'form': form})


class DeactivateUserView(UserAccountBaseView):
    """ Deactivate user account """
    template_name = 'accounts/deactivate_user.html'
    success_message = 'Your account has been deactivated.'
    success_url = 'accounts:deactivate-account'  # Replace with your success URL name

    def perform_action(self, user):
        """ Deactivate the user account """
        user.is_active = False
        user.save()


class DeleteUserView(UserAccountBaseView):
    """ Delete user account """
    template_name = 'accounts/delete_user.html'
    success_message = 'Your account has been deleted.'
    success_url = 'accounts:delete-account'  # Replace with your success URL name

    def perform_action(self, user):
        """ Delete the user account """
        user.delete()


# DONE : VERIFIED
class InActiveView(TemplateView):
    template_name = '404.html'

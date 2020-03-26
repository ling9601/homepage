from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from django.urls import reverse
from django.http import JsonResponse

from .models import User


def index(request):
    return render(request, 'users/index.html')


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.save()
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
        login(self.request, new_user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Get next url when GET or POST request
        then send it to template
        """
        context = super().get_context_data(**kwargs)
        next = self.request.GET.get(
            'next', self.request.POST.get('next', None))
        context.update({'next': next})
        return context

    def get_success_url(self):
        """ Get next_url and set it as success_url when POST request """
        next_url = self.request.POST.get('next', None)
        if next_url:
            return next_url
        else:
            return reverse('home:index')

def validate_username(request):
    """ Check if username for registration already exist """
    username = request.GET.get('username', None)
    data = {
        'is_taken':User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

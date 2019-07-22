from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'index.html')


def register(request):
    # While GET , the value of next is passed by url ,like /?next=value
    # while POST , the value of next is passed by form, like <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            # automatically login after registration
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:

        form = RegisterForm()

    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})

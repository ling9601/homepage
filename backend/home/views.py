from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.shortcuts import redirect

import subprocess
import os


def index(request):
    context = {'welcome': "Hello world"}
    return render(request, 'home/index.html', context=context)


def add(request):
    print(request)
    a = int(request.GET.get('a'))
    b = int(request.GET.get('b'))

    return JsonResponse({'result': a+b})


def debug(request):
    return render(request, 'home/debug.html')

def run_sh(request):
    if request.POST:
        # Windows
        if os.name == 'nt':
            print(request.POST.get('FileName',''))
            return HttpResponse('you are on  windows')
        # Ubuntu
        elif os.name == 'posix':
            if request.POST.get('FileName','') == 'start_jupyter_notebook.sh':
                subprocess.call('/home/ubuntu/bash/start_jupyter_notebook.sh')
            return redirect('/')

    return redirect('/')


# Create your views here.

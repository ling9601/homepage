from django.shortcuts import render
from django.http import JsonResponse


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


# Create your views here.

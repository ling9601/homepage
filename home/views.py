from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from home.utils import Code2Token


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

def get_token(request,code):
    if request.method == 'GET':
        return HttpResponse(Code2Token(code))


# Create your views here.

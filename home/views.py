from django.shortcuts import render

def index(request):
    context={'welcome':"Hello world"}
    return render(request,'home/index.html',context=context)

# Create your views here.

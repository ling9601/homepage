from django.shortcuts import render
from django.views.generic import ListView,CreateView,DetailView
from .models import Image
from django.urls import reverse_lazy
from django.shortcuts import redirect

class ImageList(ListView):
    model = Image
    template_name = 'ImageHost/ImageList.html'
    context_object_name = 'ImageList'

class upload(CreateView):
    model = Image
    template_name = 'ImageHost/upload.html'
    fields = ['title','picture']
    #upload成功後跳轉
    success_url = reverse_lazy('ImageHost:upload')

def delete(request,pk):
    if request.method=='POST':
        image=Image.objects.get(pk=pk)
        image.delete()
    return redirect(reverse_lazy('ImageHost:ImageList'))

def test(request):
    return render(request,'ImageHost/test.html')

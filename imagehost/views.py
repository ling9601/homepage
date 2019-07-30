from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from .models import Image
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .form import ImageCreateForm


class Index(ListView):
    model = Image
    template_name = 'imagehost/index.html'
    context_object_name = 'imagelist'


class ImageCreateView(CreateView):
    model = Image
    template_name = 'imagehost/upload.html'
    form_class = ImageCreateForm
    # upload成功後跳轉
    success_url = reverse_lazy('imagehost:upload')


class ImageDetailView(DetailView):
    model = Image
    template_name = 'imagehost/detail.html'
    context_object_name = 'image'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response


def delete(request, pk):
    if request.method == 'POST':
        image = Image.objects.get(pk=pk)
        image.delete()
    return redirect(reverse_lazy('imagehost:imagelist'))


def test(request):
    return render(request, 'imagehost/test.html')

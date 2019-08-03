from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, CreateView, DetailView,DeleteView
from .models import Image
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .form import ImageCreateForm


class Index(ListView):
    model = Image
    template_name = 'imagehost/index.html'
    context_object_name = 'imagelist'


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    template_name = 'imagehost/upload.html'
    form_class = ImageCreateForm
    success_url = reverse_lazy('imagehost:upload')

    def form_valid(self, form):

        form.instance.uploader=self.request.user

        if not form.instance.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')

        return super(ImageCreateView, self).form_valid(form)


class ImageDetailView(LoginRequiredMixin,DetailView):
    model = Image
    template_name = 'imagehost/detail.html'
    context_object_name = 'image'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        print(self.object.uploader)
        return response

class ImageDeleteView(LoginRequiredMixin,DeleteView):
    model=Image
    success_url=reverse_lazy('imagehost:index')


def delete(request, pk):
    if request.method == 'POST':
        image = Image.objects.get(pk=pk)
        image.delete()
    return redirect(reverse_lazy('imagehost:imagelist'))


@login_required
def test(request):
    return HttpResponse("Hello world")

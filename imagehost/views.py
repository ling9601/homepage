from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, CreateView, DetailView,DeleteView
from .models import Image,Tag,Category
from users.models import User
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .form import ImageCreateForm


class ImageListView(ListView):
    model = Image
    template_name = 'imagehost/index.html'
    context_object_name = 'image_list'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'message':'All pictures'
        })
        return context


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


class ImageDetailView(DetailView):
    model = Image
    template_name = 'imagehost/detail.html'
    context_object_name = 'image'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

class ImageDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Image
    success_url=reverse_lazy('imagehost:index')

    # prevent user delete the image that don't belong to this user
    def test_func(self):
        return self.get_object().uploader == self.request.user


class TagView(ImageListView):

    def get_queryset(self):
        self.tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))

        return super().get_queryset().filter(tags__in=[self.tag])

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'message':'Tag : {}'.format(self.tag.name)
        })
        return context

class CategoryView(ImageListView):

    def get_queryset(self):
        self.category=get_object_or_404(Category,pk=self.kwargs.get('pk'))

        return super().get_queryset().filter(category=self.category)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'message':'Category : {}'.format(self.category.name)
        })
        return context

class UploaderView(ImageListView):

    def get_queryset(self):
        self.uploader=get_object_or_404(User,pk=self.kwargs.get('pk'))

        return super().get_queryset().filter(uploader=self.uploader)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'message':'Uploader : {}'.format(self.uploader.username)
        })
        return context


@login_required
def test(request):
    return HttpResponse("Hello world")

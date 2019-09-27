from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, FormView
from .models import Image, Tag, Category
from users.models import User
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse

import PIL.Image
import PIL.ImageOps
from io import BytesIO
import base64
import os

from .form import ImageCreateForm, MultipleImageUploadForm


class ImageListView(ListView):
    model = Image
    template_name = 'imagehost/index.html'
    context_object_name = 'image_list'

    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'message': 'All pictures'
        })
        return context


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    template_name = 'imagehost/upload.html'
    form_class = ImageCreateForm
    success_url = reverse_lazy('imagehost:upload')

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        if not form.instance.make_thumbnail():
            raise Exception(
                'Could not create thumbnail - is the file type valid?')
        self.object = form.save()

        for key, value in self.request.POST.lists():
            if key == 'autotags':
                tags = []
                for tag_name in value:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    tags.append(tag)
                self.object.tags.add(*tags)

        return HttpResponseRedirect(self.get_success_url())


class ImageDetailView(DetailView):
    model = Image
    template_name = 'imagehost/detail.html'
    context_object_name = 'image'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response


class ImageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Image
    success_url = reverse_lazy('imagehost:index')

    # prevent user delete the image that don't belong to this user
    def test_func(self):
        return self.get_object().uploader == self.request.user


class TagView(ImageListView):

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))

        return super().get_queryset().filter(tags__in=[self.tag])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'message': 'Tag : {}'.format(self.tag.name)
        })
        return context


class CategoryView(ImageListView):

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs.get('pk'))

        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'message': 'Category : {}'.format(self.category.name)
        })
        return context


class UploaderView(ImageListView):

    def get_queryset(self):
        self.uploader = get_object_or_404(User, pk=self.kwargs.get('pk'))

        return super().get_queryset().filter(uploader=self.uploader)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'message': 'Uploader : {}'.format(self.uploader.username)
        })
        return context


class ImageSearchView(ImageListView):

    def get_queryset(self):
        query_set = super().get_queryset()

        search_dict = {}
        for key, value in self.request.GET.lists():
            search_dict[key] = value

        if 'category' in search_dict:
            query_set = query_set.filter(
                category__pk=search_dict['category'][0])
        if 'tags' in search_dict:
            query_set = query_set.filter(
                tags__in=search_dict['tags']).distinct()
        if 'uploader' in search_dict:
            query_set = query_set.filter(
                uploader__pk=search_dict['uploader'][0])

        x = self.request.GET.get('x')
        if x:
            query_set = query_set.filter(Q(tags__name__icontains=x) | Q(category__name__icontains=x) | Q(
                title__icontains=x) | Q(uploader__username__icontains=x)).distinct()

        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_dict = {}
        for key, value in self.request.GET.lists():
            search_dict[key] = value

        message = 'Search condition => '

        if 'category' in search_dict:
            message += 'Category: {} ;'.format(
                Category.objects.get(pk=search_dict['category'][0]).name)
        if 'tags' in search_dict:
            message += 'Tags: '
            message += ','.join(
                [tag.name for tag in Tag.objects.filter(pk__in=search_dict['tags'])])
            message += ' ;'
        if 'uploader' in search_dict:
            message += 'Uploader: {} ;'.format(
                User.objects.get(pk=search_dict['uploader'][0]).username)

        x = self.request.GET.get('x')
        if x:
            message += 'Search term: {}'.format(x)
        context.update({
            'message': message
        })

        return context


class UploadFIlesView(FormView):
    form_class = MultipleImageUploadForm
    template_name = 'imagehost/multipleupload.html'
    success_url = reverse_lazy('home:index')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')

        if form.is_valid():
            print('files ', files)
            for f in files:
                print("f ", f)
                image = Image(picture=f, uploader=request.user)
                if not image.make_thumbnail():
                    raise Exception(
                        'Could not create thumbnail - is the file type valid?')
                image.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# 必须要用post request才能接受文件, ajax中的 contenttype datatype
@csrf_exempt
def get_thumbnail(request):

    file_obj = request.FILES.get('file')
    _,file_extension=os.path.splitext(file_obj.name)

    if file_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif file_extension == '.gif':
        FTYPE = 'GIF'
    elif file_extension == '.png':
        FTYPE = 'PNG'
    else:
        return False    # Unrecognized file type

    image_data = BytesIO(file_obj.read())
    img = PIL.Image.open(image_data)

    # # get thumbnail
    img = PIL.ImageOps.fit(img, (600, 400), PIL.Image.ANTIALIAS)


    buffer = BytesIO()
    img.save(buffer, FTYPE)
    byte_data = buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode()

    return JsonResponse({'thumbnail': base64_str})

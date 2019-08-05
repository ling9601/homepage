from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from .models import Image, Tag, Category
from users.models import User
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .form import ImageCreateForm


class ImageListView(ListView):
    model = Image
    template_name = 'imagehost/index.html'
    context_object_name = 'image_list'

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

        return super(ImageCreateView, self).form_valid(form)


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

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        print('get: {}'.format(request.GET))
        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print('post: {}'.format(request.POST))
        return response


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


def search(request):

    search_dict = {}
    for key, value in request.GET.lists():
        search_dict[key] = value
    print(search_dict)

    query_set = Image.objects.all()
    message = 'Search condition => '
    if 'category' in search_dict:
        query_set = query_set.filter(category__pk=search_dict['category'][0])
        message += 'Category: {} ;'.format(
            Category.objects.get(pk=search_dict['category'][0]).name)
    if 'tags' in search_dict:
        query_set = query_set.filter(tags__in=search_dict['tags'])
        message += 'Tags: '
        message += ','.join(
            [tag.name for tag in Tag.objects.filter(pk__in=search_dict['tags'])])
        message += ' ;'
    if 'uploader' in search_dict:
        query_set = query_set.filter(uploader__pk=search_dict['uploader'][0])
        message += 'Uploader: {} ;'.format(
            User.objects.get(pk=search_dict['uploader'][0]).username)

    x=request.GET.get('x')
    print('before: ',query_set)
    if x:
        query_set=query_set.filter(Q(title__icontains=x) | Q(category__name__icontains=x))
    print('after: ',query_set)

    return render(request, 'imagehost/index.html', context={'message': message, 'image_list': query_set})


def test(request):

    search_dict = {}
    for key, value in request.GET.lists():
        search_dict[key] = value
    print(search_dict)

    # query_set=Image.objects.filter(uploader__pk=search_dict['uploader'][0]).filter(category__pk=search_dict['category'][0])
    # query_set=Image.objects.filter(tags__in=search_dict['tags'])
    # print('len: {}'.format(len(query_set)))

    query_set = Image.objects.all()
    message = ''
    if 'category' in search_dict:
        query_set = query_set.filter(category__pk=search_dict['category'][0])
        message += 'Category: {} ;'.format(
            Category.objects.get(pk=search_dict['category'][0]).name)
    if 'tags' in search_dict:
        query_set = query_set.filter(tags__in=search_dict['tags'])
        message += 'Tags: '
        message += ','.join(
            [tag.name for tag in Tag.objects.filter(pk__in=search_dict['tags'])])
        message += ' ;'
    if 'uploader' in search_dict:
        query_set = query_set.filter(uploader__pk=search_dict['uploader'][0])
        message += 'Uploader: {} ;'.format(
            User.objects.get(pk=search_dict['uploader'][0]).username)

    print(query_set)
    print(len(query_set))

    print('message: {}'.format(message))

    return HttpResponse("")

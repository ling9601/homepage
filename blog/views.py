from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

from .models import Post, Category
from comments.form import CommentForm

import markdown


class IndexView(ListView):
    model = Post

    template_name = 'blog/index.html'

    context_object_name = 'post_list'


class PostDetailView(DetailView):
    model = Post

    template_name = 'blog/detail.html'

    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        """ count number of views """
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        """ supprot markdown """
        post = super(PostDetailView, self).get_object(queryset=queryset)

        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        """ extra context_data """
        context = super(PostDetailView, self).get_context_data(**kwargs)

        context.update({
            'form': CommentForm,
            'comment_list': self.object.comment_set.all()
        })

        return context


class ArchivesView(ListView):
    model = Post

    template_name = 'blog/index.html'

    context_object_name = 'post_list'

    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                               created_time__month=self.kwargs.get('month'))


class CategoryView(ListView):
    model = Post

    template_name = 'blog/index.html'

    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))

        return super(CategoryView, self).get_queryset().filter(category=cate)


class AuthorView(ListView):
    model = Post

    template_name = 'blog/index.html'

    context_object_name = 'post_list'

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs.get('pk'))

        return super(AuthorView, self).get_queryset().filter(author=author)

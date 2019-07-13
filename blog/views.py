from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Post, Category
from comments.form import CommentForm

import markdown


def index(request):

    post_list = Post.objects.all()

    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):

    post = get_object_or_404(Post, pk=pk)

    post.increase_view()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()

    comment_list = post.comment_set.all()

    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list,
    }

    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):

    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )

    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):

    cate = get_object_or_404(Category, pk=pk)

    post_list = Post.objects.filter(category=cate)

    return render(request, 'blog/index.html', context={'post_list': post_list})

def author(request,pk):

    author=get_object_or_404(User,pk=pk)

    post_list=Post.objects.filter(author=author)

    return render(request,'blog/index.html',context={'post_list':post_list})

# Create your views here.

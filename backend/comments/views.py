from django.shortcuts import render,get_object_or_404,redirect

from blog.models import Post
from.models import Comment
from .form import CommentForm

def post_comment(request,post_pk):
    post=get_object_or_404(Post,pk=post_pk)

    if request.method=='POST':

        form=CommentForm(request.POST)

        # check form data
        if form.is_valid():

            comment=form.save(commit=False)

            comment.post=post

            comment.author = request.user

            comment.save()

            # get_absolute_url need to be implement
            return redirect(post)

        else:

            comment_list=post.comment_set.all()

            context={'post':post,
                     'form':form,
                     'comment_list':comment_list}

            return render(request,'blog/detail.html',context=context)

    # redirect to detail page if it wasn't post request
    return redirect(post)




# Create your views here.

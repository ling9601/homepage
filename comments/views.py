from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib.auth.decorators import login_required

from blog.models import Post
from.models import Comment
from .form import CommentForm

@login_required(login_url='/users/login/')
# 新增参数 parent_comment_id
def post_comment(request, post_pk, parent_comment_id=None):
    post = get_object_or_404(Post, id=post_pk)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.author
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            return redirect(post)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'post_pk': post_pk,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comments/reply.html', context)
    # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")




# Create your views here.

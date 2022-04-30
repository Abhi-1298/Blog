from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import BlogForm
from .models import Blog, Comment, Like, User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import QueryDict

# Create your views here.

def base(request):
    return render(request,'base.html','base')

def blogs(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'home.html', {"blogs": blogs,})


# from Blog model and we filter form author field which has as foreighnkey in User model
# def profile(request,user_name):
#     user_related_data = Blog.objects.filter(author__username=user_name)
#     return render(request,'home.html')




@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect('blogs')
    else:
        form = BlogForm()
        return render(request, template_name='blog_create.html', context={"form": form})


@login_required
def like_blog(request, blog_id=None):

    # print(f"This is blogid ={blog_id} and this is request.userid ={request.user.id}")

    like = Like.objects.filter(Q(blog=blog_id) & Q(user=int(request.user.id)))

    if like.exists():
        like.delete()
    else:
        like = Like(blog=Blog.objects.get(pk=blog_id),
                    user=User.objects.get(pk=int(request.user.id)))
        like.save()
    return redirect('blogs')


@login_required
def comment_blog(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        comment_body = request.POST['commentBody']
        blog = Blog.objects.get(pk=int(request.POST['blogId']))
        # this is model instance we have to pass...
        comment = Comment(body=comment_body, blog=blog,
                          user=User.objects.get(pk=request.user.id))
        comment.save()
        # print(comment)
        return JsonResponse({
            "message": "success",
            "comment": comment.as_json(),

        })



@login_required
def comment_blog(request):
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        comment_body = request.POST['commentBody']
        blog = Blog.objects.get(pk=int(request.POST['blogId']))

        # this is model instance we have to pass...
        # comment = Comment() calling like in python i.e calling a class and each field of class = to updated value of i.e what you want to save
        comment = Comment(body=comment_body, blog=blog,
                          user=User.objects.get(pk=request.user.id))
        comment.save()
        return JsonResponse({
            "message": "success",
            "comment": comment.as_json(),
        })


    # for editing the comment...
    # if put then above same thing will come like instance and model but we have to update the comment
    if request.method == "PUT":
        put = QueryDict(request.body)
        comment_body = put.get('commentBody')
        comment_id = put.get('commentId')

        # first from ajax request you got the id then with ref of that pk = id you got the id from the model
        comment = Comment.objects.get(pk=comment_id)

        # if logged in user i.e request.user is  == with comment user we can update the comment
        if request.user == comment.user:
            Comment.objects.filter(pk=comment_id).update(body=comment_body,created_at=datetime.now()) 
            comment = Comment.objects.get(pk=comment_id)

            return JsonResponse({
                "message": "success",
                "comment": comment.as_json()})

        else:
            # if rquest.user is not there then and mandetory to return anything json response
            return JsonResponse({'status': 'error',
                                 'message': 'You are not permitted to perform that action',
                                 }, status=403)














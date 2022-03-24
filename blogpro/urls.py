from django.contrib import admin
from django.urls import path
from testapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('blogs/', views.blogs, name="blogs"),
    path('blog/create/', views.create_blog, name="create_blog"),
    path('blog/like/<int:blog_id>', views.like_blog, name="like_blog"),
    path('blog/comment/', views.comment_blog, name="comment_blog"),
    # two id should come blogid and comment_id from ajax but removing thease <int:blog_id>/<int:comment.id> becuse we can take from the body 
    path('blog/comment/edit/', views.comment_blog, name="comment_blog_edit"),

    # path('blog/comment/profile/<str:user_name>', views.profile, name="profile"),
]


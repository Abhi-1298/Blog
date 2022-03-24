from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    context = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.context[:30]

    def count_likes(self):
        return self.likes.count()

    def count_comments(self):
        return self.comments.count()

    def liked_users(self):
        liked_users = self.likes.values_list('user', flat=True)
        # print("This is liked users : ",liked_users)
        return liked_users

    def get_comments(self):
        return self.comments.all().order_by("created_at")

    def pre_context(self):
        return self.context if len(self.context) < 55 else self.context[:50]+"....read more"


class Like(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.user.username}  |  >{self.blog.id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'blog'], name="unique_like"),
        ]


class Comment(models.Model):
    body = models.CharField(max_length=250)
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    # function for json
    # here we return a dictionary...
    def __str__(self):
        return f" ID :- {self.id} | Comment :- {self.body}"

    def as_json(self):
        return{
            "cmt_id": self.id,
            "body": self.body,
            "username": self.user.username,
            "created_at": self.created_at.strftime("%B-%d-%Y %H:%M%p"),
            "blog_id": self.blog.id
        }

from dataclasses import field, fields
from .models import Blog
from django.forms import ModelForm



class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['context']
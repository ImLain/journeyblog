from django.shortcuts import render
from django.urls import reverse_lazy
from django import forms

from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from posts.models import BlogPost

class BlogHome(ListView):
    model = BlogPost
    context_object_name = "posts"

    #pour ne pas afficher les articles publiés pour les visiteurs
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
            #return queryset.filter(author=self.request.user)

        return queryset.filter(published=True)



class BlogPostCreate(CreateView):
    model = BlogPost
    template_name = 'posts/blogpost_create.html'
    fields = ['title', 'content', 'published', 'images']

    def get_form(self, form_class=None):
            form = super().get_form(form_class)
            form.fields['images'].widget = forms.CheckboxSelectMultiple()
            return form

    success_url = reverse_lazy('posts:home') #ou bien dans models, on peut ajouter une fonction get_absolute_url

class BlogPostEdit(UpdateView):
    model = BlogPost
    template_name = 'posts/blogpost_edit.html'
    fields = ['title', 'content', 'published', ]

    success_url = reverse_lazy('posts:home')


class BlogPostDetail(DetailView):
    model = BlogPost
    context_object_name = "post"


class BlogPostDelete(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("posts:home")

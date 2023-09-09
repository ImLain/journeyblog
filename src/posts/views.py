from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django import forms
from .forms import PictureForm, PictureFormSet

from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from posts.models import BlogPost, Pictures

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



# class BlogPostCreate(CreateView):
#     model = BlogPost
#     template_name = 'posts/blogpost_create.html'
#     fields = ['title', 'content', 'published',]

#     success_url = reverse_lazy('posts:home') #ou bien dans models, on peut ajouter une fonction get_absolute_url



class BlogPostCreate(CreateView):
    model = BlogPost
    template_name = 'posts/blogpost_create.html'
    fields = ['title', 'content', 'published']
    success_url = reverse_lazy('posts:home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["pictures_formset"] = PictureFormSet(self.request.POST, self.request.FILES, prefix='pictures')
        else:
            data["pictures_formset"] = PictureFormSet(prefix='pictures')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pictures_formset = context["pictures_formset"]
        self.object = form.save()
        if pictures_formset.is_valid():
            pictures = pictures_formset.save(commit=False)
            for picture in pictures:
                picture.save()
                self.object.images.add(picture)
        return super().form_valid(form)


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

from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import PictureFormSet
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import Http404

from django.views import View

from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .forms import SignUpForm
from django.contrib.auth.models import User
from datetime import datetime


from posts.models import BlogPost, Pictures

User = get_user_model()


# Sign Up View
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user/signup.html'

    def get_success_url(self):
        username = self.object.username
        return reverse('posts:profile', kwargs={'username': username})

class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')

        # Si le nom d'utilisateur est vide ou non valide
        if not username or not self.is_valid_username(username):
            return redirect('home')

        return redirect('posts:profile', username=username.lower())

    def is_valid_username(self, username):
        return User.objects.filter(username=username).exists()

class BlogHome(ListView):
    model = BlogPost
    context_object_name = "posts"

    def get_queryset(self):
        # Obtenir le username depuis l'URL
        username = self.kwargs.get('username')
        # Obtenir le User object correspondant
        user = User.objects.get(username=username)

        try:
            # Obtenir le User object correspondant
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("User not found")

        # Filtrer les posts par cet utilisateur
        if self.request.user.is_authenticated and self.request.user.username == username:
            # Si l'utilisateur est authentifié et qu'il visite sa propre page, on lui montre tous ses posts
            return BlogPost.objects.filter(author=user)
        else:
            # Si un visiteur ou un autre utilisateur visite cette page, ne montrer que les posts publiés
            return BlogPost.objects.filter(author=user, published=True)

    def get_context_data(self, **kwargs):
        context = super(BlogHome, self).get_context_data(**kwargs)
        context['username_in_url'] = self.kwargs.get('username')
        return context

class BlogPostCreate(CreateView):
    model = BlogPost
    template_name = 'posts/blogpost_create.html'
    fields = ['title', 'content', 'published']

    def get_success_url(self):
        return reverse('posts:profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["pictures_formset"] = PictureFormSet(self.request.POST, self.request.FILES, prefix='pictures')
        else:
            data["pictures_formset"] = PictureFormSet(prefix='pictures')
        return data

    # def form_valid(self, form):
    #     form.instance.author = self.request.user  # Assigner l'auteur
    #     form.instance.created_on = datetime.now()

    #     context = self.get_context_data()
    #     pictures_form = context["pictures_formset"][0]  # prendre le premier formulaire du formset
    #     self.object = form.save()

    #     if pictures_form.is_valid():
    #         for file in self.request.FILES.getlist('pictures-0-img'):
    #             picture = Pictures(img=file)
    #             picture.save()
    #             self.object.images.add(picture)

    #     return super().form_valid(form)
    def form_valid(self, form):
        form.instance.author = self.request.user  # Assigner l'auteur
        form.instance.updated_on = datetime.now()

        context = self.get_context_data()
        pictures_form = context["pictures_formset"]

        self.object = form.save()

        # Supprimer toutes les anciennes images associées à ce post
        self.object.images.clear()

        if pictures_form.is_valid():
            pictures_form.instance = self.object
            pictures_form.save()

            for file in self.request.FILES.getlist('pictures-0-img'):
                picture = Pictures(img=file)
                picture.save()
                self.object.images.add(picture)

        return super().form_valid(form)

class BlogPostEdit(UpdateView):
    model = BlogPost
    template_name = 'posts/blogpost_edit.html'
    fields = ['title', 'content', 'published']

    def get_success_url(self):
        return reverse('posts:profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["pictures_formset"] = PictureFormSet(self.request.POST, self.request.FILES, prefix='pictures')
        else:
            data["pictures_formset"] = PictureFormSet(queryset=Pictures.objects.none(), prefix='pictures')
        return data

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assigner l'auteur
        form.instance.updated_on = datetime.now()

        context = self.get_context_data()
        pictures_form = context["pictures_formset"]

        self.object = form.save()

        remove_all_images = self.request.POST.get('remove_all_images', '0') == '1'
        if remove_all_images:
            self.object.images.clear()

        if pictures_form.is_valid():
            pictures_form.instance = self.object
            pictures_form.save()

            # Supprimer les anciennes images si vous le souhaitez

            for file in self.request.FILES.getlist('pictures-0-img'):
                picture = Pictures(img=file)
                picture.save()
                self.object.images.add(picture)

        return super().form_valid(form)
# class BlogPostEdit(UpdateView):
#     model = BlogPost
#     template_name = 'posts/blogpost_edit.html'
#     fields = ['title', 'content', 'published',]

#     def get_success_url(self):
#         return reverse('posts:profile', kwargs={'username': self.request.user.username})


class BlogPostDetail(DetailView):
    model = BlogPost
    context_object_name = "post"



class BlogPostDelete(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("posts:profile")
    def get_success_url(self):
        return reverse('posts:profile', kwargs={'username': self.request.user.username})

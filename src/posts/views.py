from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import PictureFormSet
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import Http404

from django.views import View

from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from posts.models import BlogPost, Pictures

User = get_user_model()

class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if username:
            return redirect('posts:home', username=username.lower())
        return reverse('posts:home', kwargs={'username': self.request.user.username})


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

class BlogPostCreate(CreateView):
    model = BlogPost
    template_name = 'posts/blogpost_create.html'
    fields = ['title', 'content', 'published', 'author', 'created_on']

    def get_success_url(self):
        return reverse('posts:home', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["pictures_formset"] = PictureFormSet(self.request.POST, self.request.FILES, prefix='pictures')
        else:
            data["pictures_formset"] = PictureFormSet(prefix='pictures')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pictures_form = context["pictures_formset"][0]  # prendre le premier formulaire du formset
        self.object = form.save()

        if pictures_form.is_valid():
            for file in self.request.FILES.getlist('pictures-0-img'):
                picture = Pictures(img=file)
                picture.save()
                self.object.images.add(picture)

        return super().form_valid(form)


class BlogPostEdit(UpdateView):
    model = BlogPost
    template_name = 'posts/blogpost_edit.html'
    fields = ['title', 'content', 'published', 'author', 'created_on']

    def get_success_url(self):
        return reverse('posts:home', kwargs={'username': self.request.user.username})


class BlogPostDetail(DetailView):
    model = BlogPost
    context_object_name = "post"



class BlogPostDelete(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("posts:home")
    def get_success_url(self):
        return reverse('posts:home', kwargs={'username': self.request.user.username})

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from model_utils.models import TimeStampedModel

User = get_user_model()


class Pictures(TimeStampedModel):
    img = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.img)

class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=255, unique=False, verbose_name="Titre")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_on = models.DateField(blank=True, null=True)
    published = models.BooleanField(default=False, verbose_name="Publié")
    content = models.TextField(blank=True, verbose_name="Contenu")
    images = models.ManyToManyField(Pictures, blank=True)

    @property
    def author_or_default(self):
        return self.author.username if self.author else "L'auteur inconnu"

    # def get_absolute_url(self):
    #     return reverse("posts:home")

    class Meta:
        ordering = ['-created_on']
        verbose_name = "Article"


    def __str__(self):
      return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.author.username}-{self.title}")
        super().save(*args, **kwargs)

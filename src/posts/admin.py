from django.contrib import admin

from posts.models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published", "created_on", "last_updated")
    list_editable = ("published",)


admin.site.register(BlogPost, BlogPostAdmin)

# Register your models here.

from django.contrib import admin

from posts.models import BlogPost, Pictures


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published", "created_on", "last_updated", "number_of_images")
    list_editable = ("published",)

    def number_of_images(self, obj):
        return obj.images.count()
    number_of_images.short_description = 'Number of Images'



admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Pictures)

# Register your models here.

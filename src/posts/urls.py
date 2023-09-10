from django.urls import path
from posts.views import BlogHome, BlogPostCreate, BlogPostEdit, BlogPostDetail, BlogPostDelete, UserSearchView, SignUpView
from django.urls import path, include

# from django.views.generic.base import TemplateView

app_name = "posts"

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # User-related URLs
    #path('signup/', SignUpView.as_view(), name='signup'),
    # path("accounts/", include("django.contrib.auth.urls")),
    path('create/', BlogPostCreate.as_view(), name="create"),

    path('<str:username>/', BlogHome.as_view(), name="profile"),
    path('search/', UserSearchView.as_view(), name="user_search"),

    # Blog post-related URLs
    path('<str:username>/<str:slug>/', BlogPostDetail.as_view(), name="post"),
    path('edit/<str:username>/<str:slug>/', BlogPostEdit.as_view(), name="edit"),
    path('delete/<str:username>/<str:slug>/', BlogPostDelete.as_view(), name="delete"),


]

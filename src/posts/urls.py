from django.urls import path
from posts.views import BlogHome, BlogPostCreate, BlogPostEdit, BlogPostDetail, BlogPostDelete

app_name = "posts"

urlpatterns = [
    #path('spongy/', BlogHome.as_view(), name="home"),
    path('', BlogHome.as_view(), name="home"),
    path('create/', BlogPostCreate.as_view(), name="create"),
    path('<str:slug>/', BlogPostDetail.as_view(), name="post"),
    path('edit/<str:slug>/', BlogPostEdit.as_view(), name="edit"),
    path('delete/<str:slug>/', BlogPostDelete.as_view(), name="delete"),
]

from django.urls import path
from . import views

app_name = 'showcase'

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),
    path('upload/', views.upload_post, name='upload'),
    path('like/<int:post_id>/', views.like_post, name='like'),
    path('comment/<int:post_id>/', views.add_comment, name='comment'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]

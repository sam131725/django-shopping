from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    """Social media post model for outfit showcase"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='showcase_posts')
    image = models.ImageField(upload_to='showcase/posts/')
    caption = models.TextField(blank=True, null=True, max_length=500)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"{self.user.username}'s post - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def total_likes(self):
        """Get total number of likes"""
        return self.likes.count()

    def total_comments(self):
        """Get total number of comments"""
        return self.comments.count()


class Comment(models.Model):
    """Comment model for posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='showcase_comments')
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"{self.user.username} commented on {self.post.user.username}'s post"

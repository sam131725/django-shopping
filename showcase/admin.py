from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption_preview', 'total_likes', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'caption')
    readonly_fields = ('created_at', 'updated_at', 'total_likes', 'total_comments')
    fieldsets = (
        ('Post Details', {
            'fields': ('user', 'image', 'caption')
        }),
        ('Engagement', {
            'fields': ('likes', 'total_likes', 'total_comments'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def caption_preview(self, obj):
        """Show preview of caption"""
        if obj.caption:
            return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
        return '(No caption)'
    caption_preview.short_description = 'Caption'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text_preview', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'text', 'post__user__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Comment Details', {
            'fields': ('post', 'user', 'text')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def text_preview(self, obj):
        """Show preview of comment text"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'

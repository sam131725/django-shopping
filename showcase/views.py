from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import Post, Comment
from .forms import PostForm, CommentForm


@login_required(login_url='login')
def feed_view(request):
    """Display all posts with comments in Instagram-style feed"""
    posts = Post.objects.all().annotate(
        comment_count=Count('comments'),
        like_count=Count('likes')
    )
    
    context = {
        'posts': posts,
        'page_title': 'Showcase Feed',
    }
    return render(request, 'showcase/feed.html', context)


@login_required(login_url='login')
def upload_post(request):
    """Handle post upload"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('showcase:feed')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'page_title': 'Upload Outfit',
    }
    return render(request, 'showcase/upload.html', context)


@login_required(login_url='login')
@require_POST
def like_post(request, post_id):
    """Like a post (AJAX support)"""
    post = get_object_or_404(Post, id=post_id)
    
    if request.user not in post.likes.all():
        post.likes.add(request.user)
        liked = True
    else:
        post.likes.remove(request.user)
        liked = False
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes()
        })
    
    return redirect('showcase:feed')


@login_required(login_url='login')
@require_POST
def add_comment(request, post_id):
    """Add comment to a post"""
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'comment': {
                'user': comment.user.username,
                'text': comment.text,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
            }
        })
    
    return redirect('showcase:feed')


@login_required(login_url='login')
def delete_post(request, post_id):
    """Delete own post"""
    post = get_object_or_404(Post, id=post_id)
    
    if request.user == post.user:
        post.delete()
    
    return redirect('showcase:feed')


@login_required(login_url='login')
def delete_comment(request, comment_id):
    """Delete own comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    
    if request.user == comment.user:
        comment.delete()
    
    return redirect('showcase:feed')


def top_posts(request, limit=5):
    """Get top posts by likes (for homepage widget)"""
    posts = Post.objects.annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:limit]
    
    return posts


def get_top_posts(limit=5):
    """Helper function to get top posts for templates"""
    return Post.objects.annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:limit]

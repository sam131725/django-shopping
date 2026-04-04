# Showcase App Integration Guide

## 🎯 Overview

The `showcase` app is now fully integrated into your Sabhachik e-commerce platform. It provides:

- 📸 Photo sharing for outfits
- ❤️ Like system with AJAX support
- 💬 Comment system
- 🎪 Instagram-style feed
- 🏆 Top posts widget for homepage

---

## 📁 File Structure

```
showcase/
├── models.py           # Post, Comment models
├── views.py            # Feed, upload, like, comment views
├── urls.py             # URL routing
├── forms.py            # PostForm, CommentForm
├── admin.py            # Admin registration
├── templates/showcase/
│   ├── feed.html       # Main feed page
│   ├── upload.html     # Upload post page
│   └── showcase_widget.html  # Homepage widget
└── migrations/
    └── 0001_initial.py # Database migrations
```

---

## 🔗 Available Routes

| Route | Purpose |
|-------|---------|
| `/showcase/feed/` | View all posts |
| `/showcase/upload/` | Upload new outfit |
| `/showcase/like/<post_id>/` | Like/unlike post (AJAX) |
| `/showcase/comment/<post_id>/` | Add comment to post |
| `/showcase/delete-post/<post_id>/` | Delete own post |
| `/showcase/delete-comment/<comment_id>/` | Delete own comment |

---

## 🏠 Homepage Integration

### Option 1: Simple Tab/Navigation (Recommended)

Add a link to the showcase feed in your navbar:

**Location:** `app/templates/app/base.html`

Add this to the navigation menu:
```html
<a href="{% url 'showcase:feed' %}" class="text-text-dark/70 hover:text-primary font-medium transition">
    Showcase
</a>
```

---

### Option 2: Show Top 5 Posts on Homepage

Add the top posts section to your homepage (`app/templates/app/index.html`):

**Step 1:** Update the view (`app/views.py`)

Find your `home` view and add this:

```python
from showcase.views import get_top_posts

def home(request):
    # ... existing code ...
    top_posts = get_top_posts(limit=5)  # Get top 5 posts
    context = {
        # ... existing context ...
        'top_posts': top_posts,
    }
    return render(request, 'app/index.html', context)
```

**Step 2:** Add the widget to your homepage template

In `app/templates/app/index.html`, add this section where you want the showcase to appear:

```html
{% include 'showcase/showcase_widget.html' %}
```

---

## 🎨 Models Overview

### Post Model
```python
class Post(models.Model):
    user = models.ForeignKey(User, ...)           # Who posted
    image = models.ImageField(...)                # The outfit photo
    caption = models.TextField(...)               # Caption text
    likes = models.ManyToManyField(User, ...)     # Who liked it
    created_at = models.DateTimeField(...)        # When posted
    updated_at = models.DateTimeField(...)        # Last updated
```

**Methods:**
- `total_likes()` - Returns count of likes
- `total_comments()` - Returns count of comments

### Comment Model
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, ...)           # Which post
    user = models.ForeignKey(User, ...)           # Who commented
    text = models.TextField(max_length=300)       # Comment text
    created_at = models.DateTimeField(...)        # When commented
```

---

## 🔐 Admin Panel

Access the admin panel to manage posts and comments:

**URL:** `/admin/`

**Features:**
- View all posts with stats (likes, comments)
- View all comments
- Delete posts/comments
- Filter by user or date
- Search functionality

---

## 🎯 Features Breakdown

### 1. Feed Page (`/showcase/feed/`)
- View all posts in a beautiful feed
- Like/unlike posts with instant feedback (AJAX)
- Add comments to posts
- Delete own posts/comments
- Empty state messaging

### 2. Upload Page (`/showcase/upload/`)
- File upload with image preview
- Caption input (max 500 chars)
- Character counter
- Image format validation
- Tips and best practices

### 3. Like System
- AJAX-powered (no page reload)
- Toggled on/off
- Real-time like count update
- Visual feedback (color change)

### 4. Comments
- Add comments to any post
- View all comments with timestamps
- Delete own comments
- Character limit (300 chars)

---

## 🛠 Customization Guide

### Change Image Upload Size Limit

In `showcase/forms.py`, modify the file widget:
```python
'image': forms.FileInput(attrs={
    'accept': 'image/*',
    # Add file size validation in view if needed
}),
```

### Change Colors

The showcase app uses your project's Tailwind theme colors:
- `primary` - #C8A27A (Beige)
- `accent` - #E8D5C4 (Cream)
- `bg-background` - #F7F3EF (Light Beige)
- `text-dark` - #3E2F23 (Dark Brown)

To customize, edit the class names in the templates.

### Change Pagination

To show more/fewer top posts on homepage, update:
```python
top_posts = get_top_posts(limit=10)  # Change 5 to desired number
```

### Add More Fields to Post

Example: Add location/tags

1. Update `showcase/models.py`:
```python
class Post(models.Model):
    # ... existing fields ...
    location = models.CharField(max_length=100, blank=True)  # NEW
```

2. Create migration:
```bash
python manage.py makemigrations showcase
python manage.py migrate showcase
```

3. Update `showcase/forms.py`:
```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption', 'location']  # ADD location
```

4. Update templates to display the new field

---

## 🚀 Performance Tips

### Optimize Image Upload

Add image compression in views:
```python
from PIL import Image

def upload_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            
            # Compress image
            img = Image.open(post.image)
            img.thumbnail((1200, 1200))
            img.save(post.image.path, quality=85)
            
            post.save()
            return redirect('showcase:feed')
```

### Add Pagination to Feed

Update `showcase/views.py`:
```python
from django.core.paginator import Paginator

def feed_view(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {'posts': posts}
    return render(request, 'showcase/feed.html', context)
```

---

## 🐛 Troubleshooting

### Images not showing?
1. Check if `MEDIA_URL` and `MEDIA_ROOT` are configured in `settings.py`
2. Ensure images are uploaded to the correct path: `showcase/posts/`
3. Check file permissions

### Likes not working via AJAX?
1. Check browser console for JavaScript errors
2. Verify CSRF token is included in form
3. Check if request header `X-Requested-With: XMLHttpRequest` is sent

### Forms not submitting?
1. Clear browser cache
2. Check for JavaScript validation errors
3. Verify CSRF token in template

---

## 📱 Mobile Responsiveness

All templates are fully responsive:
- Feed grid adapts to screen size
- Images scale properly
- Touch-friendly buttons
- Mobile navigation optimized

---

## 🔒 Security

- ✅ Uses Django authentication
- ✅ CSRF protection on all forms
- ✅ User can only delete own posts/comments
- ✅ Image upload validation
- ✅ XSS prevention via template escaping

---

## ✅ Testing Checklist

- [ ] Can upload a photo
- [ ] Caption displays correctly
- [ ] Can like/unlike post
- [ ] Can add comment
- [ ] Can delete own posts
- [ ] Can delete own comments
- [ ] Top posts show on homepage
- [ ] Is responsive on mobile
- [ ] Images display correctly
- [ ] AJAX like works without reload

---

## 📞 Support

If you encounter issues:

1. Check Django debug output in terminal
2. Review browser console for JavaScript errors
3. Verify migrations are up to date: `python manage.py migrate`
4. Clear cache: `python manage.py clear_cache`

---

## 🎉 Ready to Go!

Your showcase app is now fully integrated. Users can:
1. Navigate to `/showcase/feed/` to see all posts
2. Click "Upload Your Outfit" to share
3. Like and comment on posts
4. See top 5 posts on homepage (if integrated)

Enjoy! 🚀

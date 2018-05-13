from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CommentForm


def home(request):
    return render(request, 'home.html')


def blog(request):
    posts = Post.objects.all()
    latest_posts = [post for post in posts][-3:]
    context = {'posts': posts, 'latest_posts': latest_posts}
    return render(request, 'blog.html', context)


def post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
        related_posts = Post.objects.filter(post_type=post.post_type)[:5]
        context = {'post': post, 'related_posts': related_posts}
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('post', post_id=post.id)
    except Exception:
        return render(request, '404.html')
    return render(request, 'blog_post.html', context)

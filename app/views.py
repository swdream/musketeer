from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CommentForm


def home(request):
    posts = Post.objects.all()
    published_posts = [post for post in posts if post.status == 'Finished']
    latest_posts = published_posts[-8:]
    context = {'latest_posts': latest_posts}
    return render(request, 'home.html', context)


def blog(request):
    posts = Post.objects.all()
    published_posts = [post for post in posts if post.status == 'Finished']
    latest_posts = published_posts[-3:]
    context = {'posts': published_posts, 'latest_posts': latest_posts}
    devops_post_number = len(Post.objects.filter(category='devops'))

    sysadmin_post_number = len(Post.objects.filter(category='sysadmin'))
    developer_post_number = len(Post.objects.filter(category='developer'))
    context = {'posts': published_posts, 'latest_posts': latest_posts,
            'devops_post_number': devops_post_number,
            'sysadmin_post_number': sysadmin_post_number,
            'developer_post_number': developer_post_number}
    return render(request, 'blog.html', context)


def post(request, post_url):
    try:
        post = get_object_or_404(Post, post_url=post_url)
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

from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import PostForm
from .models import Post
from math import ceil 

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
 
def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    post = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date").first()
    return render(request, 'blog/post_list.html', {'post': post})
    # render(request, 'blog/post_list.html', {'posts': posts})
 
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_archive(request, page):    
    page=int(page)-1
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")[5*page:5*page+5] 
    posts_count = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date").count()
    pages = ceil(posts_count/5)
    pages= range(1, pages+1)
    return render(request, 'blog/post_archive.html', {'posts': posts, "posts_count": posts_count, "pages": pages})


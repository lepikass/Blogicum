from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from django.http import Http404


def index(request):
    now = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': posts})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    now = timezone.now()
    post_list = Post.objects.filter(
        category=category,
        pub_date__lte=now,
        is_published=True
    ).order_by('-pub_date')
    return render(
        request, 'blog/category.html',
        {
            'category': category,
            'post_list': post_list
        }
    )


def post_detail(request, pk):
    post = get_object_or_404(
        Post, pk=pk, is_published=True,
        pub_date__lte=timezone.now())
    if not post.category.is_published:
        raise Http404
    return render(request, 'blog/detail.html', {'post': post})

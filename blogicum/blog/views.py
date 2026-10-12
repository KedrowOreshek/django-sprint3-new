from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def index(request):
    template = 'blog/index.html'
    posts = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    ).order_by('-pub_date')[:5]
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        pk=pk,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    )
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now(),
    ).order_by('-pub_date')

    template = 'blog/category.html'
    context = {
        'category': category,
        'category_slug': category_slug,
        'posts': posts,
    }
    return render(request, template, context)

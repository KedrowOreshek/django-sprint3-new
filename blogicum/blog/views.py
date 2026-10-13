from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


POSTS_ON_MAIN_PAGE = 5


def get_published_posts():
    return Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    )


def index(request):
    template = 'blog/index.html'
    posts = get_published_posts()[:POSTS_ON_MAIN_PAGE]
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request, pk):
    post = get_object_or_404(
        get_published_posts(),
        pk=pk,
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
    posts = get_published_posts().filter(category=category)

    template = 'blog/category.html'
    context = {
        'category': category,
        'category_slug': category_slug,
        'posts': posts,
    }
    return render(request, template, context)

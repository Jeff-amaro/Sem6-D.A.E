from django.shortcuts import get_object_or_404, render

from .models import Article, Category


def home(request):
    """Show the front page with every published article."""
    articles = Article.objects.select_related('author').prefetch_related('categories')
    categories = Category.objects.all()
    context = {
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'news/home.html', context)


def article_detail(request, slug):
    """Show a single article identified by its slug."""
    article = get_object_or_404(
        Article.objects.select_related('author').prefetch_related('categories'),
        slug=slug,
    )
    return render(request, 'news/article_detail.html', {'article': article})


def category_list(request, slug):
    """Show every article that belongs to the given category."""
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.select_related('author').prefetch_related('categories')
    categories = Category.objects.all()
    context = {
        'category': category,
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'news/category_list.html', context)

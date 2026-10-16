from django.contrib import admin

from .models import Article, Author, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'article_count')
    list_filter = ('last_name',)
    search_fields = ('first_name', 'last_name', 'email')

    @admin.display(description='Articles')
    def article_count(self, obj):
        return obj.articles.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')
    list_filter = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Articles')
    def article_count(self, obj):
        return obj.articles.count()


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'category_list')
    list_filter = ('published_at', 'author', 'categories')
    search_fields = ('title', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    date_hierarchy = 'published_at'

    @admin.display(description='Categories')
    def category_list(self, obj):
        return ', '.join(category.name for category in obj.categories.all())

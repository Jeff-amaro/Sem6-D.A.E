from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Author(models.Model):
    """Person who writes the articles of the news portal."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    """Section that groups the articles by topic."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:category_list', kwargs={'slug': self.slug})


class Article(models.Model):
    """Piece of news shown in the portal."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    summary = models.TextField(blank=True)
    body = models.TextField()
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True)
    published_at = models.DateTimeField()
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='articles',
    )
    categories = models.ManyToManyField(
        Category,
        related_name='articles',
        blank=True,
    )

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug})

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, Author, Category


class NewsPortalTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name='Ana',
            last_name='Torres',
            biography='Technology writer.',
        )
        self.category = Category.objects.create(
            name='Technology',
            description='Innovation and digital culture.',
        )
        self.article = Article.objects.create(
            title='Startup launches a platform',
            summary='A short summary.',
            body='The full body of the article.',
            published_at=timezone.now(),
            author=self.author,
        )
        self.article.categories.add(self.category)

    def test_category_slug_is_generated(self):
        self.assertEqual(self.category.slug, 'technology')

    def test_article_slug_is_generated(self):
        self.assertEqual(self.article.slug, 'startup-launches-a-platform')

    def test_article_str_returns_title(self):
        self.assertEqual(str(self.article), 'Startup launches a platform')

    def test_author_str_returns_full_name(self):
        self.assertEqual(str(self.author), 'Ana Torres')

    def test_home_shows_the_article(self):
        response = self.client.get(reverse('news:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Startup launches a platform')

    def test_article_detail_shows_the_body(self):
        response = self.client.get(
            reverse('news:article_detail', args=[self.article.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The full body of the article.')

    def test_category_list_shows_the_article(self):
        response = self.client.get(
            reverse('news:category_list', args=[self.category.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Startup launches a platform')


class AutoescapeTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='Ana', last_name='Torres')
        self.article = Article.objects.create(
            title='Autoescape demo',
            body='<script>alert("xss")</script><strong>Hello</strong>',
            published_at=timezone.now(),
            author=self.author,
        )

    def test_html_in_body_is_escaped(self):
        response = self.client.get(
            reverse('news:article_detail', args=[self.article.slug])
        )
        html = response.content.decode()
        self.assertNotIn('<script>alert("xss")</script>', html)
        self.assertIn('&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;', html)
        self.assertNotIn('<strong>Hello</strong>', html)
        self.assertIn('&lt;strong&gt;Hello&lt;/strong&gt;', html)

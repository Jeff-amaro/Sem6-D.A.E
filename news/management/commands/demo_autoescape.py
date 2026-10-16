"""Prove the automatic escaping of the Django template engine.

The command stores an HTML tag in the body of a real article and then renders
the detail template to show how the page displays that tag as plain text.
"""

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from news.models import Article

SAMPLE_HTML = '<script>alert("xss")</script><strong>Hello</strong>'
START_MARKER = '<div class="article-body">'
END_MARKER = '</div>'


class Command(BaseCommand):
    help = 'Store an HTML tag in an article body and show the escaped result.'

    def handle(self, *args, **options):
        article = Article.objects.order_by('published_at').first()
        if article is None:
            self.stderr.write('No articles found. Run "seed_news" first.')
            return

        article.body = f'The editor stored this HTML: {SAMPLE_HTML}'
        article.save(update_fields=['body'])

        rendered = render_to_string(
            'news/article_detail.html',
            {'article': article},
        )
        fragment = self._extract_body(rendered)

        self.stdout.write(f'Article: {article.title}')
        self.stdout.write('')
        self.stdout.write('Stored body (in the database):')
        self.stdout.write(article.body)
        self.stdout.write('')
        self.stdout.write('HTML generated for the page:')
        self.stdout.write(fragment)
        self.stdout.write('')
        escaped = '&lt;script&gt;' in fragment and '<script>' not in fragment
        self.stdout.write(f'Tag escaped (shown as text): {escaped}')

    def _extract_body(self, rendered):
        start = rendered.find(START_MARKER)
        if start == -1:
            return rendered
        start += len(START_MARKER)
        end = rendered.find(END_MARKER, start)
        return rendered[start:end].strip()

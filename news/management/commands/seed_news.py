"""Load demonstration data for the news portal.

The command is idempotent: it can be run several times without creating
duplicated categories, authors or articles.
"""

import io
from datetime import datetime
from zoneinfo import ZoneInfo

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image, ImageDraw

from news.models import Article, Author, Category

TIME_ZONE = ZoneInfo('America/Lima')

CATEGORIES = [
    ('Politics', 'News about the government, the congress and the country.'),
    ('Sports', 'Results, transfers and stories from the sports world.'),
    ('Technology', 'Innovation, startups and digital culture.'),
]

AUTHORS = [
    (
        'Maria', 'Quispe', 'maria.quispe@newsportal.test',
        'Political reporter with ten years of experience.',
    ),
    (
        'Luis', 'Ramirez', 'luis.ramirez@newsportal.test',
        'Sports editor and football analyst.',
    ),
    (
        'Ana', 'Torres', 'ana.torres@newsportal.test',
        'Technology writer focused on artificial intelligence.',
    ),
]

ARTICLES = [
    {
        'title': 'Senate approves the new national budget',
        'category': 'Politics',
        'author': 'Maria Quispe',
        'summary': (
            'The congress passed the budget after a long debate about health '
            'and education.'
        ),
        'body': (
            'The Senate approved the new national budget for the coming year.\n'
            'The debate lasted more than six hours.'
        ),
        'published_at': '2026-09-15 08:30',
        'color': (179, 0, 27),
    },
    {
        'title': 'Mayor announces plan to renew the historic centre',
        'category': 'Politics',
        'author': 'Maria Quispe',
        'summary': (
            'The city will invest in sidewalks, lighting and green areas '
            'during the next months.'
        ),
        'body': (
            'The mayor presented the plan to renew the historic centre.\n'
            'Neighbours welcomed the initiative.'
        ),
        'published_at': '2026-09-20 10:00',
        'color': (140, 20, 30),
    },
    {
        'title': 'National team wins the regional qualifier',
        'category': 'Sports',
        'author': 'Luis Ramirez',
        'summary': (
            'A late goal gave the national team the victory in front of a '
            'full stadium.'
        ),
        'body': (
            'The national team won the regional qualifier with a goal in the '
            'last minute.\nThe crowd celebrated all night.'
        ),
        'published_at': '2026-09-22 18:45',
        'color': (12, 70, 130),
    },
    {
        'title': 'Local club signs a young striker',
        'category': 'Sports',
        'author': 'Luis Ramirez',
        'summary': (
            'The club reinforced its attack with a promising player from the '
            'youth academy.'
        ),
        'body': (
            'The local club announced the signing of a young striker.\n'
            'He will wear the number nine shirt.'
        ),
        'published_at': '2026-09-25 12:15',
        'color': (20, 90, 150),
    },
    {
        'title': 'Startup launches an artificial intelligence platform',
        'category': 'Technology',
        'author': 'Ana Torres',
        'summary': (
            'The platform helps small companies to automate their customer '
            'support.'
        ),
        'body': (
            'A local startup launched an artificial intelligence platform.\n'
            'It will help small companies to automate tasks.'
        ),
        'published_at': '2026-09-28 09:05',
        'color': (20, 120, 90),
    },
    {
        'title': 'New data centre opens in the city',
        'category': 'Technology',
        'author': 'Ana Torres',
        'summary': (
            'The data centre will host the services of several public '
            'institutions.'
        ),
        'body': (
            'A new data centre opened in the city.\n'
            'It uses renewable energy to reduce its carbon footprint.'
        ),
        'published_at': '2026-10-01 16:20',
        'color': (30, 140, 110),
    },
]


class Command(BaseCommand):
    help = 'Create three categories, three authors and six articles for the portal.'

    def handle(self, *args, **options):
        categories = self._create_categories()
        authors = self._create_authors()
        created = self._create_articles(categories, authors)
        self.stdout.write(self.style.SUCCESS(
            f'Seed finished: {len(categories)} categories, '
            f'{len(authors)} authors, {created} new articles.'
        ))

    def _create_categories(self):
        categories = {}
        for name, description in CATEGORIES:
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={'description': description},
            )
            categories[name] = category
        return categories

    def _create_authors(self):
        authors = {}
        for first_name, last_name, email, biography in AUTHORS:
            author, _ = Author.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                defaults={'email': email, 'biography': biography},
            )
            authors[f'{first_name} {last_name}'] = author
        return authors

    def _create_articles(self, categories, authors):
        created = 0
        for data in ARTICLES:
            slug = slugify(data['title'])
            if Article.objects.filter(slug=slug).exists():
                continue
            article = Article(
                title=data['title'],
                slug=slug,
                summary=data['summary'],
                body=data['body'],
                published_at=datetime.strptime(
                    data['published_at'], '%Y-%m-%d %H:%M'
                ).replace(tzinfo=TIME_ZONE),
                author=authors[data['author']],
            )
            article.save()
            article.categories.add(categories[data['category']])
            article.featured_image.save(
                f'{slug}.png',
                self._build_image(data['title'], data['color']),
                save=True,
            )
            created += 1
        return created

    def _build_image(self, title, color):
        image = Image.new('RGB', (640, 360), color)
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 280), (640, 360)], fill=(0, 0, 0))
        draw.text((20, 300), title[:48], fill=(255, 255, 255))
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        return ContentFile(buffer.getvalue())

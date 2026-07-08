from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Blog
from project.models import Project


class StaticViewSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return [
            'index',
            'about',
            'contact',
            'careers',
            'home_loan_assistance',
            'disclaimer',
            'privacy_policy',
            'terms_conditions',
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Project.objects.filter(status=True).order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class BlogSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Blog.objects.all().order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()

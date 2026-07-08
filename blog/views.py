from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Blog, BlogCategory

# Create your views here.

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'blogs'
    paginate_by = 9
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add categories for sidebar
        context['categories'] = BlogCategory.objects.all()
        # Add recent posts for sidebar
        context['recent_posts'] = Blog.objects.order_by('-created_at')[:5]
        # Add meta data for blog list page
        context['meta_title'] = 'Blog - Latest Articles and News'
        context['meta_description'] = 'Read our latest blog articles and stay updated with news'
        context['meta_keywords'] = 'blog, articles, news, real estate blog'
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog-detail.html'
    context_object_name = 'blog'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add categories for sidebar
        context['categories'] = BlogCategory.objects.all()
        # Add recent posts for sidebar
        context['recent_posts'] = Blog.objects.exclude(id=self.object.id).order_by('-created_at')[:5]
        # Add related posts (same category)
        related_categories = self.object.category.all()
        if related_categories.exists():
            context['related_posts'] = Blog.objects.filter(
                category__in=related_categories
            ).exclude(id=self.object.id).distinct()[:3]
        else:
            context['related_posts'] = Blog.objects.exclude(id=self.object.id).order_by('-created_at')[:3]
        # Add meta data
        context['meta_title'] = self.object.meta_title or self.object.name
        context['meta_description'] = self.object.meta_desc or self.object.name
        context['meta_keywords'] = self.object.keyword or ''
        return context


class BlogCategoryView(ListView):
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'blogs'
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(BlogCategory, slug=self.kwargs['slug'])
        return Blog.objects.filter(category=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = BlogCategory.objects.all()
        # Add meta data
        context['meta_title'] = self.category.title or self.category.name
        context['meta_description'] = self.category.meta_desc or f'{self.category.name} - Blog Articles'
        context['meta_keywords'] = self.category.keyword or ''
        context['recent_posts'] = Blog.objects.order_by('-created_at')[:5]
        return context

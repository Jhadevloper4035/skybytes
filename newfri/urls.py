from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from sitemaps import StaticViewSitemap, ProjectSitemap, BlogSitemap
from category import views as category_views

sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
    'blogs': BlogSitemap,
}

urlpatterns = [
    path('', include('frontend.urls')),
    path('category/', include('category.urls')),
    path('project/', include('project.urls')),
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # Sub-child category pages  e.g. /residential-project/plots-for-sale-in-sonipat/
    path('<slug:subcategory_slug>/<slug:subchild_slug>/', category_views.subchild_category_view, name='subchild_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


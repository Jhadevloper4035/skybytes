from django.contrib import admin
from blog.models import Blog, BlogCategory

# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'updated_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'meta_title', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['category']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'blog_image')
        }),
        ('Content', {
            'fields': ('overview',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_desc', 'keyword'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug')
        }),
        ('SEO', {
            'fields': ('title', 'meta_desc', 'keyword'),
            'classes': ('collapse',)
        }),
    )

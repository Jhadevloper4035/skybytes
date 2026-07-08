from django.contrib import admin
from .models import Category, SubCategory, SubChildCategory


admin.site.register(Category)
admin.site.register(SubCategory)


@admin.register(SubChildCategory)
class SubChildCategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name', 'subcategory', 'cat_slug', 'status', 'linkable')
    list_filter = ('status', 'subcategory')
    search_fields = ('cat_name', 'cat_slug')
    prepopulated_fields = {'cat_slug': ('cat_name',)}
    fieldsets = (
        ('Category Info', {
            'fields': (('cat_name', 'cat_slug'), 'subcategory', ('status', 'linkable'))
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_desc', 'meta_keyword')
        }),
        ('Page Content', {
            'fields': ('content',)
        }),
    )

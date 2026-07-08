from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class BlogCategory(models.Model):
    name = models.CharField(max_length=32, default=None)
    slug = models.SlugField(max_length=32, default=None)
    title = models.CharField(max_length=120, null=True, blank=True)
    meta_desc = models.CharField(max_length=120, null=True, blank=True)
    keyword = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:blog_category', kwargs={'slug': self.slug})

class Blog(models.Model):
    category = models.ManyToManyField(BlogCategory, related_name='BlogCategoryPost', default=None)
    name = models.CharField(max_length=225)
    slug = models.SlugField(max_length=225, unique=True)
    meta_title = models.CharField(max_length=225)
    meta_desc = models.TextField(max_length=285)
    keyword = models.CharField(max_length=164, null=True, blank=True)
    overview=RichTextUploadingField(null=True, 
                                        blank=True, 
                                        verbose_name='Project Overview',
                                        help_text=f"Type: string, Default: null, Values: Project Overview.")
    # Save blog images under MEDIA_ROOT/Blog/YYYY/MM/DD
    blog_image = models.ImageField(upload_to="Blog/%Y/%m/%d", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

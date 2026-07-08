import sys
import uuid
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Choices for category type (adjust values/labels as needed)
CATEGORY_TYPE_CHOICES = (
    (1, 'Residential'),
    (2, 'Commercial'),
    (3, 'Land'),
    (4, 'Other'),
)


class Category(models.Model):
    catType = models.IntegerField(
        choices=CATEGORY_TYPE_CHOICES,
        default=1,
        verbose_name="Category Type",
        help_text="Select category type."
    )

    cat_name = models.CharField(
        max_length=64,
        verbose_name="Category Name",
        help_text="Enter Category Name."
    )

    cat_slug = models.SlugField(
        max_length=225,
        unique=True,
        verbose_name="Category Slug",
        help_text="Enter Category Slug."
    )

    meta_title = models.CharField(
        max_length=85,
        blank=True,
        verbose_name="Category Title",
        help_text="Enter Category Meta Title (optional)."
    )

    meta_desc = models.TextField(
        max_length=165,
        blank=True,
        verbose_name="Category Description",
        help_text="Enter Category Meta Description (optional)."
    )

    meta_keyword = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Category Keyword",
        help_text="Enter Category Meta Keywords (optional)."
    )

    status = models.BooleanField(
        default=True,
        help_text="Designates whether this category should be treated as active."
    )

    linkable = models.BooleanField(
        default=True,
        help_text="Whether this category should be shown as a link."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("cat_name",)

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        # adjust 'category_detail' to the actual URL name in your app
        return reverse('category_detail', kwargs={'slug': self.cat_slug})


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='subcategories',
        on_delete=models.CASCADE,
        help_text="Select parent Category."
    )

    cat_name = models.CharField(
        max_length=32,
        verbose_name="Sub Category Name",
        help_text="Enter Sub Category Name."
    )

    cat_slug = models.SlugField(
        max_length=32,
        unique=True,
        verbose_name="Sub Category Slug",
        help_text="Enter Sub Category Slug."
    )

    meta_title = models.CharField(
        max_length=85,
        blank=True,
        verbose_name="Sub Category Title",
        help_text="Enter Sub Category Meta Title (optional)."
    )

    meta_desc = models.TextField(
        max_length=165,
        blank=True,
        verbose_name="Sub Category Description",
        help_text="Enter Sub Category Meta Description (optional)."
    )

    meta_keyword = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Sub Category Keyword",
        help_text="Enter Sub Category Meta Keywords (optional)."
    )

    status = models.BooleanField(
        default=True,
        help_text="Designates whether this subcategory should be treated as active."
    )

    linkable = models.BooleanField(
        default=True,
        help_text="Whether this subcategory should be shown as a link."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"
        ordering = ("cat_name",)

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        # adjust 'subcategory_detail' to the actual URL name in your app
        return reverse('subcategory_detail', kwargs={'slug': self.cat_slug})
    

class SubChildCategory(models.Model):

    subcategory = models.ForeignKey(SubCategory, 
                                related_name='subchild', 
                                on_delete=models.CASCADE, 
                                default=None,
                                verbose_name="Select Sub Category",
                                help_text=f"Type: Int, Values: Select Sub Category")

    cat_name=models.CharField(max_length=32,
                            default=None,
                            verbose_name="Sub Child Category Name",
                            help_text=f"Type: Int, Values: Enter Name")


    cat_slug=models.SlugField(max_length=32, unique=True,
                            default=None,
                            verbose_name="Sub Child Category Slug",
                            help_text=f"Type: Int, Values: Enter Slug")

    meta_title=models.CharField(max_length=85, null=True, blank=True,
                            verbose_name="Sub Category Title",
                            help_text=f"Type: Int, Values: Enter Meta Title")

    meta_desc=models.TextField(max_length=165, null=True, blank=True,
                            verbose_name="Category Description",
                            help_text=f"Type: String, Values: Enter Meta Description.")

    meta_keyword=models.CharField(max_length=255, null=True, blank=True,
                                verbose_name="Category Keyword",
                                help_text=f"Type: String, Values: Enter Meta Keywords.")

    content = RichTextUploadingField(null=True, blank=True,
                                     verbose_name="Page Content",
                                     help_text="Enter the main page content for this subcategory landing page.")

    status=models.BooleanField()

    linkable=models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cat_name
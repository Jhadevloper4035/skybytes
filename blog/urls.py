from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCategoryView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('category/<slug:slug>/', BlogCategoryView.as_view(), name='blog_category'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]
from django.shortcuts import render, get_object_or_404
from project.models import ProjectLinks


def subchild_category_view(request, subcategory_slug, subchild_slug):
    # Look up the ProjectLinks record whose slug matches AND whose parent SubChildCategory slug matches
    project_link = get_object_or_404(
        ProjectLinks,
        slug=subchild_slug,
        status=True,
        subchild_category__cat_slug=subcategory_slug,
    )
    projects = (
        project_link.projects
        .filter(status=True)
        .select_related('city', 'location')
        .prefetch_related('projectimage', 'category')
    )
    return render(request, 'category/subchild-category.html', {
        'project_link': project_link,
        'subcategory': project_link.subchild_category,
        'projects': projects,
    })

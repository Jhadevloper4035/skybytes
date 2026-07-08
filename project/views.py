from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Project, ProjectLead
from newfri.email_utils import send_project_lead_email

def project_list(request):
    """List published projects."""
    qs = Project.objects.filter(status=True).select_related('city').prefetch_related('category')[:100]
    return render(request, 'project/projects.html', {'projects': qs})

def project_detail(request, slug):
    """Project detail page."""
    project = get_object_or_404(Project, slug=slug, status=True)
    images = project.projectimage.all()
    floorplans = project.projectfloorplan.all()
    return render(request, 'project/project-detail.html', {
        'project': project,
        'images': images,
        'floorplans': floorplans,
        'meta_title': project.meta_title or project.name,
        'meta_description': project.meta_desc or f'{project.name} - Property Details',
        'meta_keywords': project.keyword or '',
    })


@require_POST
def submit_lead(request):
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()
    project_slug = request.POST.get('project_slug', '').strip()
    source = request.POST.get('source', 'website').strip()

    if not name or not phone:
        return JsonResponse({'success': False, 'error': 'Name and phone number are required.'}, status=400)

    project = None
    project_name = 'Not specified'
    if project_slug:
        project = Project.objects.filter(slug=project_slug).first()
        if project:
            project_name = project.name

    lead = ProjectLead.objects.create(
        project=project,
        name=name,
        email=email or None,
        phone=phone,
        message=message or None,
        source=source if source in dict(ProjectLead._meta.get_field('source').choices) else 'website',
    )

    # Send email notification
    lead_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'message': message,
        'project_name': project_name,
        'source': source.replace('_', ' ').title(),
    }
    send_project_lead_email(lead_data)

    return JsonResponse({'success': True})

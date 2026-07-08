from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from project.models import *
from blog.models import Blog
from newfri.email_utils import send_contact_form_email, send_newsletter_subscription_email, send_admin_newsletter_notification
# Create your views here.
def index(request):
    """Render the index page."""
    qs = Project.objects.all()
    # Get latest 3 blog posts for the homepage
    latest_blogs = Blog.objects.order_by('-created_at')[:3]
    return render(request, 'index.html', {'projects': qs, 'latest_blogs': latest_blogs})

def about(request):
    """Render the about page."""
    return render(request, 'pages/about-us.html')

def testimonials(request):
    """Render the testimonials page."""
    return render(request, 'pages/testimonials.html')

def gallery(request):
    """Render the gallery page."""
    return render(request, 'pages/gallery.html')

def terms_conditions(request):
    """Render the terms and conditions page."""
    return render(request, 'pages/terms-conditions-new.html')

def privacy_policy(request):
    """Render the privacy policy page."""
    return render(request, 'pages/privacy-policy-new.html')

def home_loan(request):
    """Render the home loan page."""
    return render(request, 'pages/home-loan.html')

def disclaimer(request):
    """Render the disclaimer page."""
    return render(request, 'pages/disclaimer-new.html')

def contact(request):
    """Render the contact page."""
    return render(request, 'pages/contact-us.html')


def careers(request):
    """Render the careers page."""
    # Pass an empty jobs list by default; template shows placeholders when empty.
    return render(request, 'pages/career-new.html', {'jobs': []})

def home_loan_assistance(request):
    """Render the home loan assistance page."""
    return render(request, 'pages/home-loan-assistance.html')

def construction_updates(request):
    """Render the construction updates page."""
    return render(request, 'pages/construction-updates.html')


@require_POST
def submit_contact_form(request):
    """Handle contact form submissions."""
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    inquiry_type = request.POST.get('inquiry_type', '').strip()
    message = request.POST.get('message', '').strip()

    if not all([name, email, phone, message]):
        return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

    # Send email notification to admin
    form_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'inquiry_type': inquiry_type,
        'message': message,
    }
    send_contact_form_email(form_data)

    return JsonResponse({'success': True, 'message': 'Thank you! We will get back to you soon.'})


@require_POST
def submit_newsletter(request):
    """Handle newsletter subscription."""
    email = request.POST.get('email', '').strip()

    if not email:
        return JsonResponse({'success': False, 'error': 'Email is required.'}, status=400)

    # Send welcome email to subscriber
    send_newsletter_subscription_email(email)

    # Send notification to admin
    send_admin_newsletter_notification(email)

    return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

def send_email(subject, recipient_list, html_content, text_content=None, from_email=None):
    """
    Send an email with both HTML and plain text versions.

    Args:
        subject: Email subject
        recipient_list: List of recipient emails
        html_content: HTML content of the email
        text_content: Plain text content (optional, will be stripped from HTML if not provided)
        from_email: Sender email (uses DEFAULT_FROM_EMAIL if not provided)
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    if text_content is None:
        text_content = strip_tags(html_content)

    # Debug: Log email configuration
    logger.info(f"Email Configuration:")
    logger.info(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    logger.info(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    logger.info(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    logger.info(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    logger.info(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    logger.info(f"  Sending email from {from_email} to {recipient_list}")

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=recipient_list,
        )
        msg.attach_alternative(html_content, "text/html")
        result = msg.send(fail_silently=False)
        logger.info(f"Email sent successfully! Subject: {subject}, To: {recipient_list}, Result: {result}")
        print(f"✅ Email sent successfully!")
        print(f"   Subject: {subject}")
        print(f"   To: {recipient_list}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}", exc_info=True)
        print(f"❌ Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def send_project_lead_email(lead_data):
    """
    Send email for project lead submission.

    Args:
        lead_data: Dictionary containing name, email, phone, message, project_name, source
    """
    subject = f"New Project Lead: {lead_data.get('name', 'Unknown')}"

    html_content = f"""
    <h2>New Project Lead Submission</h2>
    <p><strong>Source:</strong> {lead_data.get('source', 'Website')}</p>

    <h3>Contact Information:</h3>
    <ul>
        <li><strong>Name:</strong> {lead_data.get('name', 'N/A')}</li>
        <li><strong>Email:</strong> {lead_data.get('email', 'N/A')}</li>
        <li><strong>Phone:</strong> {lead_data.get('phone', 'N/A')}</li>
    </ul>

    <h3>Project Details:</h3>
    <ul>
        <li><strong>Project:</strong> {lead_data.get('project_name', 'Not specified')}</li>
    </ul>

    <h3>Message:</h3>
    <p>{lead_data.get('message', 'No message provided').replace(chr(10), '<br>')}</p>

    <hr>
    <p><small>This is an automated email from your website.</small></p>
    """

    recipient_list = [settings.CONTACT_EMAIL]
    return send_email(subject, recipient_list, html_content)


def send_contact_form_email(form_data):
    """
    Send email for contact form submission.

    Args:
        form_data: Dictionary containing name, email, phone, inquiry_type, message
    """
    subject = f"New Contact Form Submission: {form_data.get('inquiry_type', 'General Inquiry')}"

    html_content = f"""
    <h2>New Contact Form Submission</h2>

    <h3>Contact Information:</h3>
    <ul>
        <li><strong>Name:</strong> {form_data.get('name', 'N/A')}</li>
        <li><strong>Email:</strong> {form_data.get('email', 'N/A')}</li>
        <li><strong>Phone:</strong> {form_data.get('phone', 'N/A')}</li>
    </ul>

    <h3>Inquiry Details:</h3>
    <ul>
        <li><strong>Type of Inquiry:</strong> {form_data.get('inquiry_type', 'Not specified')}</li>
    </ul>

    <h3>Message:</h3>
    <p>{form_data.get('message', 'No message provided').replace(chr(10), '<br>')}</p>

    <hr>
    <p><small>This is an automated email from your website contact form.</small></p>
    """

    recipient_list = [settings.CONTACT_EMAIL]
    return send_email(subject, recipient_list, html_content)


def send_newsletter_subscription_email(email):
    """
    Send confirmation email for newsletter subscription.

    Args:
        email: Subscriber's email address
    """
    subject = "Welcome to SkyByte Developers Newsletter"

    html_content = f"""
    <h2>Thank You for Subscribing!</h2>
    <p>Welcome to SkyByte Developers newsletter.</p>
    <p>We're excited to keep you updated about:</p>
    <ul>
        <li>Latest construction updates and project milestones</li>
        <li>New project launches and offerings</li>
        <li>Exclusive deals and opportunities</li>
        <li>Industry insights and market trends</li>
    </ul>

    <p>If you have any questions or would like to unsubscribe, please contact us at <strong>info@skybytedevelopers.com</strong></p>

    <hr>
    <p><strong>SkyByte Developers</strong></p>
    <p>Building Tomorrow's Communities</p>
    """

    recipient_list = [email]
    return send_email(subject, recipient_list, html_content)


def send_admin_newsletter_notification(email):
    """
    Send notification email to admin for new newsletter subscription.

    Args:
        email: Subscriber's email address
    """
    subject = "New Newsletter Subscription"

    html_content = f"""
    <h2>New Newsletter Subscriber</h2>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Date:</strong> {str(__import__('datetime').datetime.now())}</p>

    <hr>
    <p><small>This is an automated email from your website.</small></p>
    """

    recipient_list = [settings.CONTACT_EMAIL]
    return send_email(subject, recipient_list, html_content)

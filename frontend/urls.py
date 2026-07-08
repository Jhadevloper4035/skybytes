from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about, name='about'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('gallery/', views.gallery, name='gallery'),
    path('construction-updates/', views.construction_updates, name='construction_updates'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('home-loan/', views.home_loan, name='home_loan'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('contact-us/', views.contact, name='contact'),
    path('submit-contact-form/', views.submit_contact_form, name='submit_contact_form'),
    path('submit-newsletter/', views.submit_newsletter, name='submit_newsletter'),
    path('careers/', views.careers, name='careers'),
    path('home-loan-assistance/', views.home_loan_assistance, name='home_loan_assistance'),
]

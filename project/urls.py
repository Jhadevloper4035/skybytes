from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('submit-lead/', views.submit_lead, name='submit_lead'),
    # path('<str:city_slug>/<str:slug>/', views.project_detail, name='project_detail'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
]

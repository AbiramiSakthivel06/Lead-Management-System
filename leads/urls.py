from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('add/', views.lead_create, name='lead_create'),
    path('<int:pk>/edit/', views.lead_update, name='lead_update'),
    path('<int:pk>/delete/', views.lead_delete, name='lead_delete'),
]

from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):
    SOURCE_CHOICES = [
        ('Web', 'Website/Form'),
        ('Referral', 'Referral'),
        ('Cold Call', 'Cold Call'),
        ('Social Media', 'Social Media'),
        ('Email Campaign', 'Email Campaign'),
        ('Other', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('In Progress', 'In Progress'),
        ('Closed Won', 'Closed Won'),
        ('Closed Lost', 'Closed Lost')
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads')
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=100)
    lead_source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='Web')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.contact_person}"

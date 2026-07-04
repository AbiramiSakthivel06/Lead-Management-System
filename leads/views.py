import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from .models import Lead
from .forms import LeadForm, UserRegistrationForm

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'leads/register.html', {'form': form})

@login_required
def dashboard(request):
    # Fetch user's leads only (strict multi-tenant check)
    leads_qs = Lead.objects.filter(owner=request.user)

    # Search filter
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    source_filter = request.GET.get('source', '').strip()

    if search_query:
        leads_qs = leads_qs.filter(
            Q(company_name__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    if status_filter:
        leads_qs = leads_qs.filter(status=status_filter)
    if source_filter:
        leads_qs = leads_qs.filter(lead_source=source_filter)

    # Get counts for KPI cards
    total_leads = leads_qs.count()
    new_leads = leads_qs.filter(status='New').count()
    in_progress = leads_qs.filter(status='In Progress').count()
    closed_won = leads_qs.filter(status='Closed Won').count()

    # Dynamic status data for Chart.js
    statuses = [choice[0] for choice in Lead.STATUS_CHOICES]
    status_counts = [leads_qs.filter(status=s).count() for s in statuses]
    
    # Dynamic source data for Chart.js
    sources = [choice[0] for choice in Lead.SOURCE_CHOICES]
    source_counts = [leads_qs.filter(lead_source=src).count() for src in sources]

    context = {
        'leads': leads_qs.order_by('-created_at'),
        'total_leads': total_leads,
        'new_leads': new_leads,
        'in_progress': in_progress,
        'closed_won': closed_won,
        'status_labels_json': json.dumps(statuses),
        'status_data_json': json.dumps(status_counts),
        'source_labels_json': json.dumps(sources),
        'source_data_json': json.dumps(source_counts),
        'search_query': search_query,
        'status_filter': status_filter,
        'source_filter': source_filter,
        'status_choices': Lead.STATUS_CHOICES,
        'source_choices': Lead.SOURCE_CHOICES,
    }
    return render(request, 'leads/dashboard.html', context)

@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.owner = request.user  # Assign current logged-in user as the lead owner
            lead.save()
            return redirect('dashboard')
    else:
        form = LeadForm()
    return render(request, 'leads/lead_form.html', {'form': form, 'title': 'Add New Lead'})

@login_required
def lead_update(request, pk):
    # Retrieve object strictly owned by current user
    lead = get_object_or_404(Lead, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'leads/lead_form.html', {'form': form, 'title': 'Edit Lead Details'})

@login_required
def lead_delete(request, pk):
    # Retrieve object strictly owned by current user
    lead = get_object_or_404(Lead, pk=pk, owner=request.user)
    if request.method == 'POST':
        lead.delete()
        return redirect('dashboard')
    return render(request, 'leads/lead_confirm_delete.html', {'lead': lead})

def csrf_failure(request, reason=""):
    return redirect('dashboard' if request.user.is_authenticated else 'login')

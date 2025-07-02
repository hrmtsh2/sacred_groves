from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import SacredGrove, PendingSacredGrove
from .forms import PendingSacredGroveForm
from django.contrib.auth.decorators import login_required
import json

def index(request): 
    return render(request, 'index.html')

def about(request): 
    return render(request, 'about.html')

def serialize_groves(queryset):
    groves = list(queryset.values(
        'name',
        'state',
        'district',
        'longitude',
        'latitude',
        'area_coverage',
        'altitude',
        'description'
    ))
    
    for grove in groves:
        grove["latitude"] = float(grove["latitude"])
        grove["longitude"] = float(grove["longitude"])
        grove["area_coverage"] = float(grove["area_coverage"]) if grove["area_coverage"] is not None else None
        grove["altitude"] = float(grove["altitude"]) if grove["altitude"] is not None else None

    return groves

def map_view(request):
    groves = serialize_groves(SacredGrove.objects.all())
    unique_states = SacredGrove.objects.values_list('state', flat=True).distinct().order_by('state')

    return render(request, 'map.html', {
        'groves_json': json.dumps(groves),
        'states': unique_states
    })

def groves_list(request):
    groves = serialize_groves(SacredGrove.objects.all())
    return JsonResponse({'groves': groves})

def submit_sacred_grove(request):
    if request.method == 'POST':
        form = PendingSacredGroveForm(request.POST)
        if form.is_valid():
            grove = form.save(commit=False)
            grove.user = request.user  # Associate the user with the submission
            grove.save()
            return redirect('grove_thank_you')  # Redirect to a thank-you page after submission
    else:
        form = PendingSacredGroveForm()

    return render(request, 'submit_grove.html', {'form': form})

@login_required
def verify_sacred_groves(request):
    if not request.user.is_staff:
        return redirect('home')  # Only allow admin users to verify groves

    pending_groves = PendingSacredGrove.objects.all()  # Get all pending submissions
    return render(request, 'verify_groves.html', {'pending_groves': pending_groves})

@login_required
def approve_sacred_grove(request, grove_id):
    if not request.user.is_staff:
        return redirect('home')  # Only allow admin users to approve groves

    try:
        pending_grove = PendingSacredGrove.objects.get(id=grove_id)
        pending_grove.move_to_verified()  # Move to the verified table
        pending_grove.delete()  # Remove from the pending table
        return redirect('verify_sacred_groves')  # Redirect back to the verify page
    except PendingSacredGrove.DoesNotExist:
        return redirect('verify_sacred_groves')  # If grove doesn't exist, go back to verify page

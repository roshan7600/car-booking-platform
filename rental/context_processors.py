from .models import Booking

def admin_context(request):
    """
    Adds admin-specific context variables to all templates
    """
    context = {}
    
    # Only add pending count if user is a superuser
    if request.user.is_authenticated and request.user.is_superuser:
        context['pending_count'] = Booking.objects.filter(status='pending').count()
    
    return context
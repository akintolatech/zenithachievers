# website/context_processors.py
from .models import WebDetails, LandingContent


def web_details(request):
    # Fetch the first WebDetails object (you can customize the query if necessary)
    details = WebDetails.objects.first()
    landing = LandingContent.objects.all()
    return {
        'business': details,
        'landing': landing
    }
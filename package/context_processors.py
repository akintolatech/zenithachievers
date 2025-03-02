# website/context_processors.py
from .models import Package


def package_list(request):
    # Fetch the first WebDetails object (you can customize the query if necessary)
    packages = Package.objects.all()

    return {
        'packages': packages,
    }
from .models import Category


def categories(request):
    return {
        'categories': Category.objects.filter(job__isnull=False).distinct()
    }

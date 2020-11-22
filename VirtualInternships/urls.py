from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('jobs:list'))),
    path('', include('pages.urls', namespace='pages')),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('admin/', admin.site.urls),
]

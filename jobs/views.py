from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404, HttpResponse
from django.views import generic

from .models import Category, Job


def index(request):
    return HttpResponse("This is the index page")


class JobListView(generic.ListView):
    model = Job
    template_name = 'jobs/list.html'


class JobCategoryListView(generic.ListView):
    model = Job
    template_name = 'jobs/category.html'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Job.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        # Call class's get_context_data method to retrieve context
        context = super().get_context_data(**kwargs)

        # context['related_jobs'] = Job.objects.filter(category=self.get_object().category).order_by('-posted')[:5]
        context['categories'] = Category.objects.filter(job__isnull=False).exclude(id=self.kwargs['pk'])
        return context


class JobDetailView(generic.DetailView):
    model = Job
    template_name = 'jobs/detail.html'

    def get_context_data(self, **kwargs):
        # Call class's get_context_data method to retrieve context
        context = super().get_context_data(**kwargs)

        context['related_jobs'] = Job.objects.filter(category=self.get_object().category).exclude(
            id=self.kwargs['pk']).order_by('posted')[:5]
        # context['related_jobs'] = Job.objects.all()
        return context


class JobSearchResultsListView(generic.ListView):
    model = Job
    template_name = 'jobs/search_results.html'

    def get_queryset(self):
        try:
            query = self.request.GET.get('q', '')
        except:
            query = ''

        if query != '':
            object_list = Job.objects.annotate(
                search=SearchVector('title', 'description', 'qualifications'),
            ).filter(search=query)
        else:
            object_list = self.model.objects.all()

        return object_list


class JobCreateView(generic.CreateView):
    model = Job
    template_name = 'jobs/create.html'
    fields = ['title', 'company', 'description', 'qualifications']

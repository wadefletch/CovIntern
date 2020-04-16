from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import JobCreationMultiForm
from .models import Category, Job


class JobListView(generic.ListView):
    model = Job
    template_name = 'jobs/list.html'
    queryset = Job.objects.all().order_by('category', '-posted', '-featured')


class JobCategoryListView(generic.ListView):
    model = Job
    paginate_by = 15
    template_name = 'jobs/category.html'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Job.objects.filter(category=category).order_by('-featured', '-posted')

    def get_context_data(self, **kwargs):
        # Call class's get_context_data method to retrieve context
        context = super().get_context_data(**kwargs)

        # context['related_jobs'] = Job.objects.filter(category=self.get_object().category).order_by('-posted')[:5]
        context['categories'] = Category.objects.filter(job__isnull=False).exclude(id=self.kwargs['pk']).distinct()
        return context


class JobDetailView(generic.DetailView):
    model = Job
    template_name = 'jobs/detail.html'

    def get_context_data(self, **kwargs):
        # Call class's get_context_data method to retrieve context
        context = super().get_context_data(**kwargs)

        context['related_jobs'] = Job.objects.filter(category=self.get_object().category).exclude(
            id=self.kwargs['pk']).order_by('-posted')
        # context['related_jobs'] = Job.objects.all()
        return context


class JobSearchResultsListView(generic.ListView):
    model = Job
    template_name = 'jobs/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['query'] = self.request.GET.get('q', '')
        except:
            context['query'] = ''

        return context

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
    form_class = JobCreationMultiForm
    template_name = 'jobs/job_form.html'

    def get_success_url(self):
        return reverse('jobs:detail', kwargs={'pk': self.object['job'].pk})


class AboutView(generic.TemplateView):
    template_name = 'jobs/about.html'


class StatusView(generic.TemplateView):
    template_name = 'jobs/status.html'

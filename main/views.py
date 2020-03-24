from django.shortcuts import render, reverse
from django.views import generic

from .forms import MailchimpSubscribeForm
from .utils import SendSubscribeMail


class IndexFormView(generic.FormView):
    form_class = MailchimpSubscribeForm
    template_name = 'main/index.html'
    success_url = reverse('jobs:index')

    def form_valid(self, form):
        SendSubscribeMail(form.cleaned_data['email'])
        return super().form_valid(form)


def about(request):
    return render(request, 'main/about.html')

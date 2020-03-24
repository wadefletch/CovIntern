from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexFormView.as_view(), name='index'),
    path('about/', views.about, name='about'),
]

app_name = 'main'

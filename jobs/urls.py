from django.urls import path

from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.JobDetailView.as_view(), name='detail'),
    path('category/<int:pk>/', views.JobCategoryListView.as_view(), name='category'),
    path('search/', views.JobSearchResultsListView.as_view(), name='search_results'),
    path('create/', views.JobCreateView.as_view(), name='create'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('status/', views.StatusView.as_view(), name='status')
]

app_name = 'jobs'

from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
]

app_name = 'auth'

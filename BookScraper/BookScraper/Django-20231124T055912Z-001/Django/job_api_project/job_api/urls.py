from django.urls import path
from .views import create_job, index

urlpatterns = [
    path('jobs/', create_job, name='create_job'),
    path('index/', index, name='index'),
]

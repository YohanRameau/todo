from django.urls import path

from . import views

app_name = 'task'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<str:section_name>/', views.section, name='section'),
    path('<str:section_name>/<str:task_name>', views.task, name='task'),
]


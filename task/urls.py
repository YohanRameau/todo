from django.urls import path

from . import views

app_name = 'task'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<str:section_name>/', views.section, name='section'),
    path('<str:section_name>/<str:task_name>', views.task, name='task'),
    path('create_section',views.create_section, name='create_section'),
    path('delete_section/<str:section_name>/', views.delete_section, name='delete_section'),
    path('create_task',views.create_task, name='create_task'),
    path('delete_task/<str:section_name>/<str:task_name>',views.delete_task, name='delete_task'),
]
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Section, Task

# Index will be showed the five sections who have the most recent task.
def index(request):
    section_list = sorted(Section.objects.all(), key=lambda s: s.more_recent_task_date())[:5]
    tasks_set = [s.task_set.all() for s in [section for section in section_list]]
    context = {
        'section_list'  : section_list,
        'tasks_set' : tasks_set, 
    }
    return render(request, 'task/index.html', context)

# This fonction will be showed all task of the named section.
def section(request, section_name: str):
    section = get_object_or_404(Section,name=section_name)
    #section = Section.objects.get(name=section_name)
    return render(request, 'task/section.html',{'section':section})

def task(request, section_name: str, task_name: str):
    section = get_object_or_404(Section,name=section_name)
    try:
        task = section.task_set.get(name=task_name)
    except Task.DoesNotExist:
        raise Http404(f"Task {task_name} does not exist.")
    return render(request, 'task/task.html', {'task': task})


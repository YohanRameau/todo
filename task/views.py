from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Section, Task


# Index will be showed the five sections who have the most recent task.
def index(request:HttpRequest) -> HttpResponse:
    """ This method provide main todo page view

    :param request: 
    :type request: HttpRequest
    :return: HttpResponse with a context include all sections
    :rtype: HttpResponse
    """
    section_list = sorted(Section.objects.all(), key=lambda s: s.more_recent_task_date())[:5]
    tasks_set = [s.task_set.all() for s in [section for section in section_list]]
    context = {
        'section_list'  : section_list,
        'tasks_set' : tasks_set, 
    }
    return render(request, 'task/index.html', context)


# This fonction will be showed all task of the named section.
def section(request:HttpRequest, section_name: str) -> HttpResponse:
    """[summary]

    :param request: [description]
    :type request: [type]
    :param section_name: [description]
    :type section_name: str
    :return: [description]
    :rtype: HttpResponse
    """
    section = get_object_or_404(Section,name=section_name)
    #section = Section.objects.get(name=section_name)
    
    return render(request, 'task/section.html',{'section':section})


def task(request:HttpRequest, section_name: str, task_name: str) -> HttpResponse :
    section = get_object_or_404(Section,name=section_name)
    try:
        task = section.task_set.get(name=task_name)
    except Task.DoesNotExist:
        raise Http404(f"Task {task_name} does not exist.")
    return render(request, 'task/task.html', {'task': task})


def create_section(request:HttpRequest) -> HttpResponse:
    section_name = request.POST['section_name']
    Section(name=section_name).save()
    return index(request)


def create_task(request:HttpRequest) -> HttpResponse:
    
    return index(request)
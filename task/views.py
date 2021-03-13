from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse

from urllib.parse import ParseResult, urlparse

from .models import Section, Task


# Index will be showed the five sections who have the most recent task.
def index(request: HttpRequest) -> HttpResponse:
    """ This method provide main todo page view

    :param request: 
    :type request: HttpRequest
    :return: HttpResponse with a context include all sections
    :rtype: HttpResponse
    """
    section_list = sorted(Section.objects.all(
    ), key=lambda s: s.more_recent_task_date(), reverse=True)[:5]
    context = {
        'section_list': section_list,
    }
    return render(request, 'task/index.html', context)


# This fonction will be showed all task of the named section.
def section(request: HttpRequest, section_name: str) -> HttpResponse:
    """[summary]

    :param request: [description]
    :type request: [type]
    :param section_name: [description]
    :type section_name: str
    :return: [description]
    :rtype: HttpResponse
    """
    section = get_object_or_404(Section, name=section_name)
    context = {
        'title': section.name,
        'section': section,
        'tasks': section.tasks
    }
    #section = Section.objects.get(name=section_name)

    return render(request, 'task/section.html', context)


def task(request: HttpRequest, section_name: str, task_name: str) -> HttpResponse:
    section = get_object_or_404(Section, name=section_name)
    try:
        task = section.task_set.get(name=task_name)
    except Task.DoesNotExist:
        raise Http404(f"Task {task_name} does not exist.")
    return render(request, 'task/task.html', {'task': task})


def create_section(request: HttpRequest) -> HttpResponse:
    section_name = request.POST['section_name']
    Section(name=section_name).save()
    return HttpResponseRedirect(reverse('task:index'))

def delete_section(request: HttpRequest,section_name: str) -> HttpResponse:
    s: Section = Section.objects.get(name=section_name)
    s.delete()
    return HttpResponseRedirect(reverse('task:index'))

def create_task(request: HttpRequest) -> HttpResponse:
    section_name = request.POST.get("section_name")
    task_name = request.POST["task_name"]
    deadline = request.POST["task_date"] if request.POST["task_date"] != "" else None
    task_section = Section.objects.get(name=section_name)
    path = urlparse(request.headers['Referer']).path
    try:
        Task(name=task_name, deadline=deadline, section=task_section).save()
    except:
        return HttpResponseRedirect(path)
    else:
        return HttpResponseRedirect(path)


def delete_task(request: HttpRequest, task_name: str, section_name: str) -> HttpResponse:
    path = urlparse(request.headers['Referer']).path
    s: Section = Section.objects.get(name=section_name)
    t: Task = Task.objects.get(name=task_name, section=s)
    print("task", t)
    t.delete()
    return HttpResponseRedirect(path)

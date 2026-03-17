from django.http import HttpResponse
from .models import Task
from django.shortcuts import render
def hello(request):
    all_tasks = Task.objects.all()
    task_list = ", ".join([t.title for t in all_tasks])

    return HttpResponse(f"Database says: {task_list}")

def index(request):
    return render(request, 'main/index.html')
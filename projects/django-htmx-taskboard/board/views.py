from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from .forms import TaskForm
from .models import Task


def task_context(request, form=None):
    active = request.GET.get("filter", request.POST.get("filter", "all"))
    if active not in ("all", "open", "done"):
        active = "all"
    tasks = Task.objects.all()
    if active == "open":
        tasks = tasks.filter(done=False)
    elif active == "done":
        tasks = tasks.filter(done=True)
    return {
        "tasks": tasks,
        "form": form or TaskForm(),
        "active": active,
        "open_count": Task.objects.filter(done=False).count(),
        "total_count": Task.objects.count(),
    }


@require_GET
def home(request):
    return render(request, "board/home.html", task_context(request))


@require_GET
def list_tasks(request):
    return render(request, "board/_task_list.html", task_context(request))


@require_POST
def add_task(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        form.save()
        response = render(request, "board/_task_list.html", task_context(request))
        response["HX-Trigger"] = "taskAdded"
        return response
    # Return a full form fragment to keep errors visible in the UI.
    response = render(request, "board/_form.html", {"form": form})
    response["HX-Retarget"] = "#task-form"
    return response


@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save(update_fields=["done"])
    return render(request, "board/_task_list.html", task_context(request))


@require_POST
def delete_task(request, pk):
    get_object_or_404(Task, pk=pk).delete()
    return render(request, "board/_task_list.html", task_context(request))

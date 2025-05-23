from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Task
from django.db.models import Q, Count
from django.contrib import messages


# Create your views here.
def manager_dashboard(request):
    type = request.GET.get("type", "all")
    # print("\n\n", type, "\n\n")

    base_query = Task.objects.select_related("details").prefetch_related("assigned_to")
    if type == "Completed":
        tasks = base_query.filter(status="COMPLETED")
    elif type == "In-Progress":
        tasks = base_query.filter(status="IN_PROGRESS")
    elif type == "Pending":
        tasks = base_query.filter(status="PENDING")
    elif type == "all":
        tasks = base_query.all()

    counts = Task.objects.aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(status="COMPLETED")),
        pending=Count("id", filter=Q(status="PENDING")),
        in_progress=Count("id", filter=Q(status="IN_PROGRESS")),
    )

    context = {"tasks": tasks, "counts": counts}
    return render(request, "dashboard/manager-dashboard.html", context)


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def test(request):
    context = {
        "names": ["aru", "fihu", "sharu", "maru"],
        "age": 20 + 18,
    }
    return render(request, "test.html", context)


def create_task(request):
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST":
        """django Model form"""
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Created Task Successfully")

            return redirect("create-task")

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)
    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":
        """django Model form"""
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Update Task Successfully")

            return redirect("update-task", id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Delete Successfully... ")
        return redirect("manager-dashboard")
    else:
        messages.error(request, "something went wrong... ")
        return redirect("manager-dashboard")


def view_task(request):
    task = Task.objects.all()
    return render(request, "view_tasks.html", {"tasks": task})

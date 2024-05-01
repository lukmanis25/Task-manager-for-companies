from django.shortcuts import render, redirect
from .forms import RegisterForm, TaskForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Task
from django.db.models import Q


@login_required(login_url="/login")
def home(request):
    tasks = Task.objects.filter(Q(manager=request.user) | Q(worker=request.user))

    if request.method == "POST":
        task_id = request.POST.get("task-id")
        if task_id:
            task = Task.objects.filter(id=task_id).first()
            if task and task.manager == request.user:
                task.delete()

    return render(request, 'main/home.html', {"tasks": tasks})


@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.manager = request.user
            task.save()
            return redirect("/home")
    else:
        form = TaskForm()

    return render(request, 'main/create_task.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
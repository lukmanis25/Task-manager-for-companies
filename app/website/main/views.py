from django.shortcuts import render, redirect
from .forms import RegisterForm, TaskForm, UpdateTaskManagerForm, UpdateTaskForm
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
@permission_required("main.add_task", login_url="/login", raise_exception=True)
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

    form.fields['worker'].queryset = get_valid_workers()
    return render(request, 'main/create_task.html', {"form": form})

@login_required(login_url="/login")
def update_task(request, pk):

    task = Task.objects.get(id=pk)

    if request.user == task.manager:
        form = UpdateTaskManagerForm(instance=task)
        form.fields['worker'].queryset = get_valid_workers()
    else:
        form = UpdateTaskForm(instance=task)

    if request.method == 'POST':
        form = UpdateTaskManagerForm(request.POST, instance=task) if request.user == task.manager else UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("/home")

    return render(request, 'main/update_task.html', {"form": form})

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

def get_valid_workers():
    manager_group = Group.objects.get(name='manager')
    managers = manager_group.user_set.all()
    admin = User.objects.get(username='admin')
    return User.objects.exclude(id__in=managers.values_list('id', flat=True)).exclude(id=admin.id)
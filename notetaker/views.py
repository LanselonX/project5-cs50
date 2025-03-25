from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from .models import User, Task, Team, Invitation
from .forms import AddTasksForm, AddTeamForm
from django.db.models import Q  
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

@login_required(login_url='login')
def index(request):
    user = request.user

    user_tasks = Task.objects.filter(
        team__isnull=True,
        task_author=user
    ).exclude(status='done')

    team_tasks = Task.objects.filter(assigned_to=user).exclude(status='done').distinct()

    return render(request, 'notetaker/index.html', {
        'user_tasks': user_tasks,
        'team_tasks': team_tasks,
    })

def create_invitation(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.user != team.team_author:
        return JsonResponse({'error': 'You are not a team member'}, status=403)
    
    invitation = Invitation.objects.create(team=team)
    invitation_link = request.build_absolute_uri(f"/join_team/{invitation.token}/")

    return JsonResponse({'invitation_link': invitation_link})

def join_team(request, token):
    invitation = get_object_or_404(Invitation, token=token)
    team = invitation.team

    if request.user not in team.member.all():
        team.member.add(request.user)

    return redirect('user_team')

def user_team(request):
    user = request.user
    teams = Team.objects.filter(Q(team_author=user) | Q(member=user)).distinct()

    paginator = Paginator(teams, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notetaker/teams.html', {
        'teams': page_obj,
    })

def create(request):
    if request.method == 'POST':
        form = AddTasksForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_author = request.user
            task.save()
            return redirect("index")
    else:
        form = AddTasksForm()
    return render(request, 'notetaker/create_tasks.html', {
        "taskForm": form,
    })

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, task_author=request.user)

    if request.method == 'POST':
        form = AddTasksForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddTasksForm(instance=task)
    
    return render(request, 'notetaker/edit_task.html', {
        "taskForm": form,
        "task": task,
    })

def mark_task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.team:
        if request.user != task.team.team_author and request.user != task.assigned_to:
            return JsonResponse({'error': 'Permission error'}, status=403)

    else:
        if request.user != task.task_author:
            return JsonResponse({'error': 'Permission error'}, status=403)
        
    task.status = 'done'
    task.save()
    return JsonResponse({'success': True})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.team:
        if request.user != task.team.team_author and request.user != task.assigned_to:
            return JsonResponse({'error': 'Permission error'}, status=403)
        
    else:
        if request.user != task.task_author:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
    task.delete()
    return JsonResponse({'success': True})

def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    if request.user != team.team_author:
        return JsonResponse({'error': 'Permission error'})

    team.delete()
    return JsonResponse({'success': True})

def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.user == team.team_author:
        return JsonResponse({'error': "the team leader can't leave" }, status=403)

    Task.objects.filter(team=team, assigned_to=request.user).delete()

    if request.user in team.member.all():
        team.member.remove(request.user)

    return redirect('user_team')

def assign_task(request, team_id, task_id):
    team = get_object_or_404(Team, id=team_id)
    task = get_object_or_404(Task, id=task_id, team=team)

    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    if request.user not in team.member.all() and request.user != team.team_author:
        return JsonResponse({'error': 'No permission'}, status=403)

    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'error': "user_id is required"}, status=400)

        user = User.objects.get(id=user_id)
        if not team.member.filter(id=user.id).exists() and user != team.team_author:
            return JsonResponse({'error': 'User is not in the team'}, status=404)

        task.assigned_to = user
        task.save()

        return JsonResponse({'success': True, 'assigned_to': user.username})
    except (User.DoesNotExist, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid data'}, status=400)
        
def create_team_task(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.user not in team.member.all() and request.user != team.team_author:
        return redirect('index')
    
    if request.method == 'POST':
        form = AddTasksForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_author = request.user
            task.team = team
            task.save()
            return redirect('team_detail', team_id=team.id)
    else:
        form = AddTasksForm()
    return render(request, 'notetaker/create_team_task.html', {
        "teamTask": form,
        "team": team,
    })

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.user not in team.member.all() and request.user != team.team_author:
        return render(request, 'notetaker/user_team.html', {
            "message": "Error request to get team"
        })
    
    tasks_todo = team.tasks.filter(status='todo')
    tasks_in_progress = team.tasks.filter(status='in_progress')
    tasks_done = team.tasks.filter(status='done')

    if request.method == 'GET':
        return render(request, 'notetaker/task_detail.html', {
            'tasks_todo': tasks_todo,
            'tasks_in_progress': tasks_in_progress,
            'tasks_done': tasks_done,
            'team': team,
        })
    else:
        return render(request, 'notetaker/task_detail.html', {
            "message": "Unsupported request method"
        })

def solo_task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, task_author=request.user)

    task_data = {
        'id': task.id,
        'title': task.title, 
        'image': task.image.url if task.image else None,
        'description': task.description,
    }
    return JsonResponse(task_data)

def task_detail_api(request, team_id, task_id):
    team = get_object_or_404(Team, id=team_id)
    task = get_object_or_404(team.tasks, id=task_id)

    if request.user not in team.member.all() and request.user != team.team_author:
        return JsonResponse({'error': 'request error - task detail'}, status=403)
    
    task_data = {
        'id': task.id,
        'title': task.title, 
        'description': task.description,
        'image': task.image.url if task.image else None,
    }
    return JsonResponse(task_data)

def create_team(request):
    if request.method == 'POST':
        form = AddTeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.team_author = request.user
            team.save()
            team.member.add(request.user)
            return redirect("user_team")
    else:
        form = AddTeamForm()
    return render(request, 'notetaker/create_team.html', {
        "teamForm": form,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "notetaker/login.html", {
                "message": "Invalid username or password"
            })
    else:
        return render(request, "notetaker/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:
            return render(request, "notetaker/register.html", {
                "message": "Password is incorrect"
            })
        
        try: 
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "notetaker/register.html", {
                "message": "Username already taken"
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "notetaker/register.html")
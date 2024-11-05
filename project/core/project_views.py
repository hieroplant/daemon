from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Project

def home(request):
    projects = Project.objects.all()
    return render(request, 'core/index.html', {'projects': projects})

def create_project(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if Project.objects.filter(name__iexact=name).exists():
            return render(request, 'core/createproject.html', {'error': 'Project with this name already exists.'})
        
        Project.objects.create(name=name, description=description)
        return render(request, 'core/createproject.html', {'success': 'Project created successfully.'})
    
    return render(request, 'core/createproject.html')

def check_project_name(request):
    name = request.GET.get('name', '').upper()
    exists = Project.objects.filter(name__iexact=name).exists()
    return JsonResponse({'exists': exists})

def delete_project(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return redirect('home')
    return redirect('home')
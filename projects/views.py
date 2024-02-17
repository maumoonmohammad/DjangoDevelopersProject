from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProjects, paginateProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage




def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
   

    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range }
    return render(request,'projects/projects.html',context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    tags = projectObj.tags.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit= False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount
        return redirect('project', pk=projectObj.id)
       
    return render(request,'projects/single-project.html',{'project': projectObj, 'tags': tags,'form': form})

@login_required(login_url="login")   # a user should be logged in to create a project or he will be redirected to login page
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES) # request.FILES is for processing the incoming images
        if form.is_valid():
            project = form.save(commit = False)
            project.owner = profile  # we are linking the project to the user logged in because owner to project has one to many relationship 
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
                
                
            return redirect('account')   ## will go back to projects remember in url patterns we have name='projects'
    context = {'form': form}
    return render(request,'projects/project_form.html',context)


@login_required(login_url='login')
def updateProject(request,pk):
    profile = request.user.profile #get the profile of th euser first and then based on the profile we will get the project that way its more safe
    project = profile.project_set.get(id=pk) # we are quering only a specific users profile 
    form = ProjectForm(instance=project) # instance = project all the fields of the data would be pre filled

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        
        form = ProjectForm(request.POST, request.FILES, instance = project) #again which project are we updating instance = project
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
                return redirect('update-project', pk=project.id)

            return redirect('account')   ## will go back to projects remember in url patterns we have name='projects'
    context = {'form': form,'project': project}
    return render(request,'projects/project_form.html',context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('account')
    context= {'object':project}
    return render(request,'delete_template.html',context)
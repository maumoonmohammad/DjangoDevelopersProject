from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles
from .models import Profile, Message
from .forms import CustomUserCreationForm,ProfileForm, SkillForm, MessageForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


def profiles(request):
    profiles,search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 6)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html',context)

def userProfile(request,pk):
    user = Profile.objects.get(id=pk)
    topskills = user.skill_set.exclude(description__exact = "") #here skill is a child element of a user(profile) we are excluding the skill whose description is empty, simply the user left it blank
    otherskills = user.skill_set.filter(description="")# include all the skills that have description
    context = {'user':user,'topskills':topskills,'otherskills':otherskills}
    return render(request,'users/user-profile.html',context)

def LoginUser(request):
    page = 'login'
    if request.user.is_authenticated: # if the user is logged in and wants to go to login page by changing the address like /login directly he cant go there because hw should be logged out to go to the login page
       return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            
                user = User.objects.get(username = username)
        except:
            messages.error(request,'Username does not exist')
            print('Username does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)  #login will create a session in the database and store it into cookies of the browser for user authentication
            return redirect(request.GET['next'] if 'next' in request.GET else 'account') # send the user to the next route
        else:
            messages.error(request,'Username or Password is incorrect')
        
    return render(request,'users/login_register.html')

def logoutUser(request): # for logging out the user, it simply deletes the session stored in the cookies and database
    logout(request)
    messages.error(request,'User was logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False) # the commit holds the user in the user instance to modify the form details
            user.username = user.username.lower() # dont want the username to be case sensitive
            user.save()

            messages.success(request,'User account was created!')
            
            login(request,user)# creates a session for this user

            return redirect('edit-account')
        else:
            messages.error(request,'An error has occured for some reason')
    context = {'page':page,'form': form}
    return render(request,'users/login_register.html',context)


@login_required(login_url = 'login') # this decprator is for the user to be logged in and if the user is not logged in they will be directed to login page
def userAccount(request):
    profile = request.user.profile # this gives us the profile of the logged in user
    skills = profile.skill_set.all() #here skill is a child element of a user(profile) we are excluding the skill whose description is empty, simply the user left it blank
    projects = profile.project_set.all()

    context = {'profile': profile,'skills': skills,'projects':projects}
    return render(request, 'users/account.html', context)

@login_required(login_url = 'login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance = profile)  #instance = profile fills out the already existing info

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False) #creating an instance before actually saving
            skill.owner = profile  #linking the skill to tha specific owner
            skill.save()
            return redirect('account')
    context = {'form':form}
    return render(request,'users/skill_form.html',context)


@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile

    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance = skill)
    if request.method == 'POST':
        form = SkillForm(request.POST,instance = skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {'object': skill}
    return render(request,'delete_template.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all() #remember we didnt write messages_set because in our models we have the attribute related_name='messages' 
    unreadCount = messageRequests.filter(is_read = False).count()
    context = {'messageRequests':messageRequests, 'unreadCount': unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id = pk)
    if message.is_read == False:
        message.is_read = True # just updating the is_read attribute if the message has been opened
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile # if the user is logged in or not
    except:
        sender = None # here user wont be logged in, hence we have sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            return redirect('user-profile',pk = recipient.id)


    context = {'recipient':recipient,'form':form}
    return render(request,'users/message_form.html',context)
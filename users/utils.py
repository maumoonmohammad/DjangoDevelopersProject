from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):

    page = request.GET.get('page')
    # results = 3  # the number of results you want to display per page

   

    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.page(page)
    
    except PageNotAnInteger:   # this exception is to display the first page otherwise we would get an error
        page = 1
        profiles = paginator.page(page)

    except EmptyPage: # if the page entered manually is exceeds the number of pages we have
        page = paginator.num_pages # this gives us the last page
        profiles = paginator.page(page)

    
    leftIndex = (int (page) - 4)


    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int (page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    
    custom_range = range(leftIndex, rightIndex) #left and right index are only set to customize the number of pages at the bottom if we have 1000 pages we f=dont wanna have all the 1000 buttons at the same time


    return custom_range, profiles



def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):  # here search_query is the name attribut from the front end
        search_query = request.GET.get('search_query')
        
    skills = Skill.objects.filter(name__icontains = search_query)

    profiles = Profile.objects.distinct().filter(    #distinct makes sure we dont get copies of users because if we search by skills. We get only one instance of each user.
        Q(name__icontains = search_query) | 
        Q(short_intro__icontains = search_query) |
        Q(skill__in = skills) #checks if this profile has these skills associated with it
        ) #name__icontains using this does not worry about case sensitivity 'name' is actually the dynamic value here it could be short_intro_icontains  'model field' is followed by icontains, Q is the auery to add the  | (or) condition

    return profiles, search_query




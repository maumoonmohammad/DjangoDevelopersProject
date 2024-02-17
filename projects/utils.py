from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, results):

    page = request.GET.get('page')
    # results = 3  # the number of results you want to display per page

   

    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
    
    except PageNotAnInteger:   # this exception is to display the first page otherwise we would get an error
        page = 1
        projects = paginator.page(page)

    except EmptyPage: # if the page entered manually is exceeds the number of pages we have
        page = paginator.num_pages # this gives us the last page
        projects = paginator.page(page)

    
    leftIndex = (int (page) - 4)


    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int (page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    
    custom_range = range(leftIndex, rightIndex) #left and right index are only set to customize the number of pages at the bottom if we have 1000 pages we f=dont wanna have all the 1000 buttons at the same time


    return custom_range, projects







def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):  # here search_query is the name attribut from the front end
        search_query = request.GET.get('search_query')


    tags = Tag.objects.filter(name__icontains = search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) | 
        Q(description__icontains = search_query) | 
        Q(owner__name__icontains = search_query) |
        Q(tags__in = tags) # the tags on the right side is a field in models because many to many relation
    )
    return projects, search_query



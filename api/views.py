from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project,Review, Tag



@api_view(['GET'])  ## the below view will only accept GET requests, we could also add more options like POST, PUT but those are not required at the moment
def getRoutes(request):

    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},


        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]

    return Response(routes)  # returns data in Json format


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many = True) # we cannot pass the projects directly in a context dictionary because we need to serialize it first

    return Response(serializer.data)


@api_view(['GET'])
def getProject(request,pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # This means the user has to be authenticated, it basically requires JWT to process the view below
def projectVote(request,pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile   # this user we are getting from tokens 
    data = request.data # the data that we send

    review, created = Review.objects.get_or_create( #sees if the user is already voted or not if the user is already present it would get the user oyherwise it will create
        owner = user,
        project = project,
    )

    review.value = data['value']
    review.save()
    project.getVoteCount # getVoteCount is a function and its called normally because its defined by @property decorator 
    
    serializer = ProjectSerializer(project, many= False)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']
    project = Project.objects.get(id = projectId)
    tag = Tag.objects.get(id = tagId)
    project.tags.remove(tag)
    return Response('Tag was deleted')

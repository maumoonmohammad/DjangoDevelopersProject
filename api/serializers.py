from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer): # its just like a model form to specify what fields we need to output when somebody makes an api call
    owner = ProfileSerializer(many=False) # gives us the owner of the project without this we were only getting owner id in json data
    tags = TagSerializer(many = True)
    reviews = serializers.SerializerMethodField() # To create a method we need to write this line of code, we have created a method below
    


    class Meta:
        model = Project
        fields = '__all__' 


    def get_reviews(self,obj): #here obj is the project
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many= True)
        return serializer.data
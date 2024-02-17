from django.db import models
from django.contrib.auth.models import User # importing the inbuilt user model in django to have
                                            # a one to one relationship with the created profile
                                            # so that each user has only one profile. We create a 
                                            # separate profile because we do not want to mess up the
                                            # inbuilt user model that will affect the whole application
import uuid
# Create your models here.




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank= True)  # if user is deleted the profile gets deleted
    name = models.CharField(max_length=200, blank=True, null = True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png') #upload_to goes into profile folder in static/images
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False )


    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['created']
    
    @property
    def imageURL(self): #if we deleted an image of a project we were getting an error, our website was breaking thats why this method was written
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url



class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False )

    def __str__(self):
        return str(self.name) #returns the name of the table in admin panel
    


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete = models.SET_NULL, null  = True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete = models.SET_NULL, null  = True, blank=True, related_name = 'messages') # related_name is just to distinguish from the upper line of the code
    name = models.CharField(max_length=200, null=True, blank = True)
    email = models.CharField(max_length=200, null=True, blank = True)
    subject = models.CharField(max_length=200, null=True, blank = True)
    body = models.TextField()
    is_read = models.BooleanField(default = False, null=True) # if the message has been read or not
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False )


    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read', '-created']
    

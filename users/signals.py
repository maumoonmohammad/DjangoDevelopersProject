from django.db.models.signals import post_save, post_delete   #used for signals (its an action that triggers an event)
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender, instance, created, **kwargs): # creating a signal function sender is the model which sends the signal and instance is the object(someone's profile) of the same model and created is gonna be True or Flase(if an existing user is updated) suggesting if the user was craeted or not.
   if created:              # if a new user (created would be true)
       user = instance
       profile = Profile.objects.create( # creates a profile for a user automatically once the user is created otherwise we had to create a user first and then a profile for them, because we have a one to one relation between user and profile
           user = user,
           username = user.username,
           email = user.email,
           name = user.first_name,
       )
       subject = 'Welcome to DevSearch'
       message = 'We are happy to have you on our Platform'
       send_mail(
           subject,
           message,
           settings.EMAIL_HOST_USER,
           [profile.email],
           fail_silently=False
       )

    


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user #one to one relationship, we can access it both ways
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()






def deleteuser(sender, instance,**kwargs):
    try:
     user  = instance.user # if we delete the profile the user doesnt get deleted because in one to one relationshp if we delete the user the profile gets deleted but not the opposite, so to delete the user when profile is deleted we have written this code.
     user.delete()
    except:
       pass
    


post_save.connect(createProfile, sender = User) # this command triggers the function that is create profile once a profile is created, here the sender model is User
post_save.connect(updateUser,sender = Profile)


post_delete.connect(deleteuser,sender=Profile)
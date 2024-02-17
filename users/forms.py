
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm): # we are inheriting from UserCreationForm and it would have all the functionalities of the inherited form
    class Meta:
        model = User #we imported it 'User' because it is a user model form
        fields = ['first_name', 'email' , 'username', 'password1', 'password2']
        labels = {      #used to change the names that are in the fields variable.
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

              # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add title'}) # 'input here is the css class for design'
        
        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add description'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'}) 


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email', 'username',
                  'location', 'bio','short_intro','profile_image',
                    'social_github','social_linkedin', 'social_youtube', 'social_twitter']
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

              # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add title'}) # 'input here is the css class for design'
        
        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add description'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'}) 


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

              # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add title'}) # 'input here is the css class for design'
        
        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add description'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'}) 



class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

              # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add title'}) # 'input here is the css class for design'
        
        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add description'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'}) 
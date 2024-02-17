from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm (ModelForm):
    class Meta:
        model = Project    ## creating a form for Project table in models
        fields = ['title','description','demo_link','source_link','featured_image']
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

              # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add title'}) # 'input here is the css class for design'
        
        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add description'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

  


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body' ]
        labels = {      #used to change the names that are in the fields variable.
            'value': 'Place your vote',
            'body': 'Add your comment here',
        }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

              # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add title'}) # 'input here is the css class for design'
        
        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add description'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
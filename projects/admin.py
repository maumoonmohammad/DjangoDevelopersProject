from django.contrib import admin
from .models import Project, Review, Tag

admin.site.register(Project)  # this piece of code shows this table in the admin panel
admin.site.register(Review)
admin.site.register(Tag)


# Register your models here.

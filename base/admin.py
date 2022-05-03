from django.contrib import admin
# added manually
from base.models import Contact
from .models import Question, Comment


# Register your models here.
# This is registering for contacts page
admin.site.register(Contact)
# This is rigistering for questions page
admin.site.register(Question)
# This is rigistering for answering page
admin.site.register(Comment)
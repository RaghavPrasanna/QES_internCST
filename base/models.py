from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse

# Create your models here.

# To put contacts details in django database
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    # This is to know the date
    date = models.DateField()

# To change contact.object to name

    def __str__(self):
        return self.name

# For adding Questions
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    content = models.TextField(null=True, blank=True)
    # For upVote 
    likes = models.ManyToManyField(User, related_name='question_post')
    # For downVote
    dislikes = models.ManyToManyField(User, related_name='question_posta')
    date_created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f'{self.user.username} - Question'

    def get_absolute_url(self):
        return reverse('question-detail', kwargs = {'pk':self.pk})
    
    # for upVote
    def total_likes(self):
        return self.likes.count()
    
    # for downVote
    def total_dislikes(self):
        return self.dislikes.count()



# This is for asking answers
class Comment(models.Model):
    question = models.ForeignKey(Question, related_name="comment", on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    content = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.question.title, self.question.user)

    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk':self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'), 

    # This is to display the questions 
    path('questions/', views.QuestionListView.as_view(), name ="question-lists"),
    path('questions/new/', views.QuestionCreateView.as_view(), name ="question-create"),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name="question-detail"),
    path('questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name="question-update"),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name="question-delete"),
    path('questions/<int:pk>/comment/', views.AddCommentView.as_view(), name="question-comment"),
    path('like/<int:pk>', views.like_view, name="like_post"),
    path('dislike/<int:pk>', views.dislike_view, name="dislike_post"),


    
]

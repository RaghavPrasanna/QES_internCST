from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from datetime import datetime
from base.models import Contact
from django.contrib import messages

# These are used for displaying, updating Question and answers
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
# This prevents users from editing the questions of other users 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Question, Comment

from .forms import CommentForm
from django.urls import reverse, reverse_lazy

# Create your views here.

# This is for upVote
def like_view(request, pk):
    post = get_object_or_404(Question, id=request.POST.get('question_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        # remove
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('question-detail', args=[str(pk)]))

# This is for downVote
def dislike_view(request, pk):
    post = get_object_or_404(Question, id=request.POST.get('question_id'))
    disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        # remove
        post.dislikes.remove(request.user)
        disliked = False
    else:
        post.dislikes.add(request.user)
        disliked = True
    return HttpResponseRedirect(reverse('question-detail', args=[str(pk)]))


# This is used to List the questions on the website
class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']

# For searching in nav bar
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['questions'] = context['questions'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context

# This is used to display the question on the website
class QuestionDetailView(DetailView):
    model = Question

    # For upVote 
    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data()
        something = get_object_or_404(Question, id=self.kwargs['pk'])
        total_likes = something.total_likes()
        liked = False
        if something.likes.filter(id=self.request.user.id).exists():
            liked = True
        total_dislikes = something.total_dislikes()
        disliked = False
        if something.dislikes.filter(id=self.request.user.id).exists():
            disliked=True


        context['total_likes'] = total_likes
        context['liked'] = liked
        context['total_dislikes'] = total_dislikes
        context['disliked'] = disliked
        return context
    
    # For downVote 
    
# This is used to create questions/answers
class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# This is used to update the question 
class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False

#    This is used to delete the questions
class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name =  'question'
    success_url = "/"

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False

# This is used to answer questions
class CommentDetailView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'base/question-detail.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('question-detail')

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    
    template_name = 'base/question-answer.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('question-lists')

   





         
def home(request):
    # return HttpResponse("Hello world")
    return render(request,'home.html')

def contact(request):
#    To store in database
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent! We will Contact you Soon.')
    return render(request, 'contact.html')


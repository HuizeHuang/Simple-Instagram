from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from Insta.models import Post, Like, Comment
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from Insta.forms import CustomUserCreationForm


class HelloWorld(TemplateView):
    template_name = 'helloworld.html'

class PostView(ListView):
    model = Post
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):  # LoginRequiredMixin must be before CreateView
    model = Post
    template_name = 'post_create.html'
    fields = "__all__"
    login_url = "login"


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    form_class = CustomUserCreationForm   #combine fields and model
    template_name = 'registration/signup.html'
    success_url = reverse_lazy("login")


@ajax_request  #this is an ajax request, showing it doesn't need to render a template
def toggleLike(request):
    '''come from index.js in static/js'''
    post_pk = request.POST.get('post_pk')

    # find the current post
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()  # might throws Exception if there is already a like with the same post and user
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0
    return {
        'result': result, 
        'post_pk': post_pk
    }

@ajax_request
def addComment(request):
    '''come from index.js in static/js'''
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    comment_text = request.POST.get('comment_text')
    commenter_info = {}

    try:
        comment = Comment(post=post, user=request.user, comment=comment_text)
        comment.save()  # might throws Exception if there is already a like with the same post and user
        result = 1
        commenter_info = {
            'username': request.user.username,
            'comment_text': comment_text
        }
    except Exception as e:
        print(e)
        result = 0
    
    return {
        'result': result, 
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }
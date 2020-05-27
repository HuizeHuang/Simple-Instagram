from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from Insta.models import Post, Like, Comment, CustomUser, UserConnection
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from Insta.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


class HelloWorld(TemplateView):
    template_name = 'helloworld.html'


class PostView(ListView):
    model = Post
    template_name = 'index.html'

    # @login_required
    def get_queryset(self):
        '''we are overriding the super function in the ListView to 
        redefine the object_list (post objects) that is going to be passed to index.html'''
        if self.request.user.is_authenticated:
            following_users = set()
            current_user = self.request.user

            # it's equivalent to the query:
            # SELECT to_user FROM UserConnection WHERE from_user = current_user
            for conn in UserConnection.objects.filter(from_user = current_user).select_related('to_user'):
                following_users.add(conn.to_user)

            # it's equivalent to the query:
            # WHERE author IN following_users
            return Post.objects.filter(author__in = following_users)
        else:
            return super().get_queryset()
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        liked = Like.objects.filter(post=self.kwargs.get('pk'), user=self.request.user).first()
        if liked:
            data['liked'] = 1
        else:
            data['liked'] = 0
        return data


class PostCreateView(LoginRequiredMixin, CreateView):  # LoginRequiredMixin must be before CreateView
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'image']
    login_url = "login"


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("/")


class SignUp(CreateView):
    form_class = CustomUserCreationForm   #combine fields and model
    template_name = 'registration/signup.html'
    success_url = reverse_lazy("login")


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'user_detail.html'
    login_url = 'login'


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'user_update.html'
    fields = ['profile_pic', 'username']
    login_url = 'login'


class ExploreView(ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'
    
    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]

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


@ajax_request
def toggleFollow(request):
    follow_user_pk = request.POST.get('follow_user_pk')
    to_user = CustomUser.objects.get(pk=follow_user_pk)
    from_user = CustomUser.objects.get(pk=request.user.id)
    try:
        if from_user != to_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(from_user=from_user, to_user=to_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(from_user=from_user, to_user=to_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0
    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }
        
from django.db import models
from imagekit.models import ProcessedImageField     #doc: https://django-imagekit.readthedocs.io/en/latest/
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


# Create your models here.
# after creating new models, remember to migrate

class CustomUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles',
        format = 'JPEG',
        options = {'quality': 100},
        blank = True,
        null = True
    )
    def get_followers(self):
        # filter() returns all objects that matched, get() only returns one object
        return UserConnection.objects.filter(to_user=self)  # they all return connections, not users

    def get_followings(self):
        return UserConnection.objects.filter(from_user=self)

    def is_followed_by(self, user):
        '''check if current user is followed by second given user'''
        connections = get_followers(self)  # it returns connections, not users
        return connections.filter(from_user=user).exists()

    def __str__(self):
        return self.username


class UserConnection(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='from_connections'
    )
    to_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='to_connections'
    )
    def __str__(self):
        return self.from_user.username + " follows " + self.to_user.username


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality': 100},
        blank = True,
        null = True
    )
    posted_on = models.DateTimeField(
        auto_now_add=True
    )
    def get_like_count(self):
        return self.likes.count()
    
    def get_comment_count(self):
        return self.comments.count()

    def get_absolute_url(self):
        '''
        whenever a new post is made, the link will be redirected to the url defined below
        '''
        return reverse("post_detail", args=[str(self.id)])  # find the full url based on the name provided

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'   # post.likes --> Select all users FROM Like WHERE post = current post
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return 'Likes: ' +  self.user.username + ' likes ' + self.post.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Comment from ' + self.user.username + ': ' + self.comment
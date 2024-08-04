from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    followers = models.ManyToManyField('self', blank=True, null=True, related_name="followers")
    number_of_followers = models.IntegerField(default=0)
    following = models.ManyToManyField('self', blank=True, null=True, related_name="following")
    number_of_following = models.IntegerField(default=0)


class Posts(models.Model):

    content = models.CharField(max_length=250)
    user_posting = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_posting")
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    user_liking = models.ManyToManyField(User, blank=True, null=True, related_name="liked_posts")

    def __str__(self):
        return f"{self.user_posting} posted on {self.created_at}"

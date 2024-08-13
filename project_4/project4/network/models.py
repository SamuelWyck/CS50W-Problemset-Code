from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    @property
    def number_followers(self):
        all_followers = self.followers.all()
        if not all_followers:
            return 0
        return len(all_followers)
    
    @property
    def number_following(self):
        all_following = self.following.all()
        if not all_following:
            return 0
        return len(all_following)
        
        
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    content = models.CharField(max_length=400, null=False)
    timestamp = models.DateTimeField(auto_now=True)
    @property
    def likes(self):
        all_likes = self.post_likes.all()
        if not all_likes:
            return 0
        return len(all_likes)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")


class Follow(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
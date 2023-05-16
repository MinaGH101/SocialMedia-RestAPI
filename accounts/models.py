from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save


class Post(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts') 
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.slug} - {self.created}'
    
    
    def get_absolute_url(self):
        return reverse("home:post", args=(self.id, self.slug)) 
    
    def like_counter(self):
        return self.post_votes.count()
    
    
class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.from_user} following {self.to_user}'
    
    
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comment', blank=True, null=True) # it is related to Comments model.
    
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} - {self.body[:20]}'
    


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_votes')
    
    def __str__(self):
        return f'{self.user} liked {self.post}' 


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.SmallIntegerField(default=0)
    bio = models.CharField(max_length=100, null=True, blank=True)
    
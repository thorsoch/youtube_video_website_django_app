from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    name = models.CharField(max_length = 100)
    video_id = models.CharField(max_length = 20, unique = True)
    url = models.URLField()
    thumb = models.URLField()
    likes = models.IntegerField(default = 0)
    uploaded = models.DateTimeField(null = True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    name = models.CharField(max_length = 30, null = True)
    user_id = models.IntegerField()
    text = models.TextField()
    video_id = models.CharField(max_length = 20)
    posted = models.DateTimeField(null = True)

    def __str__(self):
        return "Comment by " + self.name

class Tag(models.Model):
    name = models.CharField(max_length = 30)
    video_id = models.CharField(max_length = 20)

    def __str__(self):
        return self.video_id + " is in " + self.name

class Like(models.Model):
    name = models.IntegerField()
    video_id = models.CharField(max_length = 20)
    timestamp = models.DateTimeField(null = True)

    def __str__(self):
        return str(self.name) + " likes " + self.video_id

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Requesto(models.Model):
    text = models.TextField()
    user_id = models.IntegerField()

    def __str__(self):
        return self.text
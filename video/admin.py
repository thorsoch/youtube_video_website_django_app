from django.contrib import admin
from video.models import Video, Comment, Like, Tag, Requesto
from video.models import UserProfile

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(UserProfile)
admin.site.register(Requesto)
admin.site.register(Tag)
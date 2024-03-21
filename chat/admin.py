from django.contrib import admin
from .models import  Room, Message, UserGroupLeftInfo

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(UserGroupLeftInfo)
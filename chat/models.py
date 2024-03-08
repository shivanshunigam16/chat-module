from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Room(models.Model):

    PUBLIC = 'public'
    PRIVATE = 'private'
    PERSONAL = 'personal'
    
    ROOM_TYPE = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('personal', 'Personal')
    )
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=100)
    room_type = models.CharField(
        max_length=50, choices=ROOM_TYPE,
        default=PUBLIC,
        verbose_name=_('Room Type'),
    )
    members = models.ManyToManyField(
        User, related_name="member",
        blank=True,
        verbose_name="Member of Group"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,null=True,
        related_name="created_rooms",
        verbose_name="Created By"
    )


    def __str__(self):
        return "Room : "+ self.name + " | Id : " + self.slug
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to ='uploads/',blank=True, null=True)

    def __str__(self):
        return "Message is :- "+ self.content
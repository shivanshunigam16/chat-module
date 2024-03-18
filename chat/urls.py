from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import Home, SignUpView, RoomDetail, AddRoomViewset, DeleteRoom, GroupMembers

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='regi'),
    path("<str:slug>/<int:pk>", RoomDetail.as_view(), name='room-detail'),
    path("addroom/", AddRoomViewset.as_view(), name='room'),
    path('delete-room/<int:pk>/', DeleteRoom.as_view(), name='delete_room'),
    path('group-members/<int:pk>/', GroupMembers.as_view(), name='members'),
    path('group-members/<int:pk>/remove-user/<int:user_id>/', GroupMembers.as_view(), name='remove_user'),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
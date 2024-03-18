from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import AddRoomForm, UserRegistrationForm
from .models import Message, Room, User
from django.db.models import Q


class SignUpView(CreateView):
    """
    View for user sign-up.
    This view allows users to sign up using the UserRegistrationForm.
    Upon successful registration, users are redirected to the login page.
    """
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class Home(View):
    def get(self, request):
        room = Room.objects.filter(
            Q(room_type='public') | 
            Q(Q(room_type='private') & Q(members=self.request.user)) |
            Q(created_by=self.request.user)
        )
        return render(request, "home.html", {'rooms': room, 'is_home_page':True})


class RoomDetail(View):
    """
    View for displaying room details.
    This view retrieves the room and associated messages from the
    database and renders the room detail template
    with the room information and messages.
    """
    def get(self, request, slug, pk):
        room = get_object_or_404(Room, id=pk, slug=slug)
        messages = Message.objects.filter(room=room).select_related('user')

        context = {
            "room_name": room.name,
            "room_type": room.room_type,
            "slug": slug,
            "room_id": pk,
            'messages': messages
        }

        return render(request, "room.html", context)


class AddRoomViewset(CreateView):
    """
    Viewset for adding a new room.
    This view allows users to create a new room using the AddRoomForm.
    Upon successful creation, users are redirected to the home page.
    """
    template_name = 'addform.html'
    form_class = AddRoomForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        room_instance = form.save(commit=False)
        selected_members_ids = self.request.POST.getlist('members')
        selected_members_ids.append(self.request.user.id)
        selected_members = User.objects.filter(pk__in=selected_members_ids)
        room_instance.created_by = self.request.user
        room_instance.save()
        room_instance.members.add(*selected_members)
        room_instance.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Retrieves context data for the template.
        This method fetches all users to display them
        as options for room members.
        """
        context = super().get_context_data(**kwargs)
        context['all_users'] = User.objects.all()
        return context


class DeleteRoom(View):
    def post(self, request, pk):
        """
        View for deleting a room.
        This view allows users to delete a room.
        Only the user who created the room can delete it.
        """
        try:
            room = Room.objects.get(id=pk)
            # Check if the current user created the room
            if room.created_by == request.user:
                room.delete()
                return JsonResponse({"message": "Room Deleted Successfully"})
            else:
                return JsonResponse(
                    {"error": "You are not authorized to delete this room."},
                    status=403
                )

        except Room.DoesNotExist:
            return JsonResponse({"error": "Room not found."}, status=404)


class GroupMembers(View):
    """
    View for managing group members.
    This view allows users to retrieve and modify
    group members for a specific room.
    """
    def get(self, request, pk):
        """
        Handles the GET request to retrieve
        group members for a specific room.
        """
        try:
            room = Room.objects.get(id=pk)
            users_in_room = room.members.all()
            user_list = [
                {
                  'id': user.id,
                  'username': user.username
                } for user in users_in_room
            ]
            return JsonResponse({'users': user_list})
        except Room.DoesNotExist:
            return JsonResponse(
                {'error': 'Room does not exist'},
                status=404
            )

    def post(self, request, pk, user_id):
        """
        Handles the POST request to remove a user from the group.
        """
        try:
            room = Room.objects.get(id=pk)
            user = room.members.filter(id=user_id).first()
            if user:
                room.members.remove(user)
                return JsonResponse(
                    {'message': 'User removed from the room successfully'}
                )
            else:
                return JsonResponse(
                    {'error': 'User not found in the room'},
                    status=404
                )
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room does not exist'}, status=404)

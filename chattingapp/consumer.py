import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from chat.models import Room,Message,User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.roomGroupName = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room_id = text_data_json["room_id"]
        room_name = text_data_json["room_name"]
        image = text_data_json["image"]
    
        await self.save_message(message, username, room_name,room_id, image)     
        await self.channel_layer.group_send(
        self.roomGroupName, {
            "type": "sendMessage",
            "message": message,
            "username": username,
            "room_name": room_name,
            "image": image
        }
    )
        
        
    
    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        image =  event["image"]
        await self.send(text_data=json.dumps({"message": message, "username": username, "image":image}))
       
    
    @sync_to_async
    def save_message(self, message, username, room_name, room_id, image):
        user=User.objects.get(username=username)
        room=Room.objects.get(id=room_id,name=room_name)
        
        Message.objects.create(user=user,room=room,content=message, image=image)
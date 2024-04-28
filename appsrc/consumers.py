# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    def create_chat(self,message, sender_id):
                    
            from .models import ChatRoom_Model, User_Message, User
            User_Message.objects.create(
                chat_room=ChatRoom_Model.objects.get(room_name=self.room_name),
                sender_id=User.objects.get(id=int(sender_id)),
                message_text=message
            )
            
    # def send_notifications(self, sender_id, sender_name):
    #     from .models import UserRoom, Notification, User
    #     user_rooms = UserRoom.objects.values_list("user__id","id").filter(Q(chat_room__room_name = self.room_name) & ~Q(user__id = int(sender_id)))
        
    #     content = f"New Message From {sender_name}"
    #     href = f"messages/?room={self.room_name}"
    #     for u_id in user_rooms:
    #         u_room = UserRoom.objects.get(id = u_id[1])
    #         u_room.unseen_messages += 1
    #         u_room.last_updated = datetime.now()
    #         u_room.save()
            
    #         Notification.objects.create(
    #             text = content,
    #             src_url = href,
    #             user = User.objects.get(id = u_id[0])
    #         )
        

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.create_chat(message,text_data_json['sender'])
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, "sender":text_data_json['sender']}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        sender_id = event['sender']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message,'sender':sender_id}))
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Room, Message


# class ChatConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
#         await self.channel_layer.group_add(self.room_name, self.channel_name)

#         await self.accept()

#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.room_name, self.channel_name)
#         self.close(code)

#     async def receive(self, text_data):
#         # print("Recieved Data")
#         data_json = json.loads(text_data)
#         # print(data_json)

#         event = {"type": "send_message", "message": data_json}

#         await self.channel_layer.group_send(self.room_name, event)

#     async def send_message(self, event):
#         data = event["message"]
#         await self.create_message(data=data)

#         response = {"sender": data["sender"], "message": data["message"]}

#         await self.send(text_data=json.dumps({"message": response}))

#     @database_sync_to_async
#     def create_message(self, data):
#         get_room = Room.objects.get(room_name=data["room_name"])

#         if not Message.objects.filter(
#             message=data["message"], sender=data["sender"]
#         ).exists():
#             new_message = Message.objects.create(
#                 room=get_room, message=data["message"], sender=data["sender"]
#             )

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Room, Message

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.group_name = f"chat_{self.room_name}"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         sender = data['sender']

#         # Save message in DB
#         await self.save_message(sender, self.room_name, message)

#         # Send message to group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': sender,
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender'],
#         }))


#     async def send_message(self, event):
#         data = event["message"]
#         await self.create_message(data=data)

#         # Send flat data, not nested
#         await self.send(text_data=json.dumps({
#             "message": data["message"],
#             "sender": data["sender"],
#         }))


#     @database_sync_to_async
#     def save_message(self, sender, room_name, message):
#         room, _ = Room.objects.get_or_create(room_name=room_name)
#         Message.objects.create(room=room, sender=sender, message=message)

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Room, Message

# class ChatConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.group_name = f"chat_{self.room_name}"

#         self.user = self.scope["user"]
#         self.user_group = f"user_{self.user.username}"

#         # Join room group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         # Join user notification group
#         await self.channel_layer.group_add(
#             self.user_group,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)
#         await self.channel_layer.group_discard(self.user_group, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)

#         message = data["message"]
#         sender = data["sender"]
#         receiver = data["receiver"]

#         # Save message
#         await self.save_message(sender, receiver, self.room_name, message)

#         # Send chat message to room
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "chat_message",
#                 "message": message,
#                 "sender": sender,
#             }
#         )

#         # 🔔 Send notification to receiver
#         await self.channel_layer.group_send(
#             f"user_{receiver}",
#             {
#                 "type": "notify",
#                 "sender": sender,
#                 "message": message,
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "chat",
#             "sender": event["sender"],
#             "message": event["message"],
#         }))

#     async def notify(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "notification",
#             "text": f"{event['sender']} sent you a message",
#             "sender": event["sender"],
#             "message": event["message"],
#         }))

#     @database_sync_to_async
#     def save_message(self, sender, receiver, room_name, message):
#         room, _ = Room.objects.get_or_create(room_name=room_name)
#         Message.objects.create(
#             room=room,
#             sender=sender,
#             receiver=receiver,
#             message=message
#         )
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name')
        self.sender = self.scope["user"].username

        users = self.room_name.split("_")
        if len(users) == 2 and users[0] == users[1]:
            await self.close()
            return

        self.group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # ✅ SEND JOIN MESSAGE AS NOTIFICATION (NOT CHAT)
        for user in users:
            if user != self.sender:
                await self.channel_layer.group_send(
                    f"user_{user}",
                    {
                        "type": "notify",
                        "sender": self.sender,
                        "message": "joined the chat",
                    }
                )

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = self.sender
        receiver = data.get("receiver")
        room_name = data.get("room_name")
        message = data.get("message")

        # Save message
        await self.save_message(sender, receiver, room_name, message)

        # Send to room group
        await self.channel_layer.group_send(
            f"chat_{room_name}",
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            }
        )

        # Send notification to receiver
        await self.channel_layer.group_send(
            f"user_{receiver}",
            {
                "type": "notify",
                "sender": sender,
                "message": message,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "sender": event["sender"],
            "message": event["message"],
        }))

    async def notify(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "text": f"{event['sender']} sent you a message",
            "sender": event["sender"],
            "message": event["message"],
        }))

    @database_sync_to_async
    def save_message(self, sender, receiver, room_name, message):
        room, _ = Room.objects.get_or_create(room_name=room_name)
        Message.objects.create(
            room=room,
            sender=sender,
            receiver=receiver,
            message=message
        )

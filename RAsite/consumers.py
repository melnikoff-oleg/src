# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
import json
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from users.models import Chat3, Message, CustomUser

#User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user_pk = self.scope['url_route']['kwargs']['user_pk']
        self.user = CustomUser.objects.get(pk = self.user_pk)

        #suppose
        if self.user.is_renter:
            for landlord in self.user.clients.all():
                chat = landlord.chat3
                room_group_name = "chat" + str(chat.pk)
                async_to_sync(self.channel_layer.group_add)(
                    room_group_name,
                    self.channel_name
                )

        self.accept()
    
    def preLoadChats(self, author_pk): 
        chats_list = []
        for landlord in self.user.clients.all():
            chat = landlord.chat3
            chats_list.append(self.chat_to_json(chat, author_pk))
        content = {
                'command': 'preload_chats',
                'chats': chats_list
            }
        self.send_message(content)
    
    def chat_to_json(self, chat, author_pk):
        chat_size = len(chat.users.all())
        return {
            'name' : chat.name,
            'pk' : chat.pk,
            'size' : chat_size,
            'messages' : self.messages_to_json(chat.messages.order_by('-timestamp').all(), author_pk),
        }

    def messages_to_json(self, messages, author_pk):
        result = []
        for message in messages:
            result.append(self.message_to_json(message, author_pk))
        return result

    def message_to_json(self, message, author_pk):
        return {
            'author': message.author,
            'content': message.content,
            'time': message.getTime(),
            'pk': message.pk,
            'author_pk': author_pk,
        }

    def new_message(self, data):
        text_message = data['message']
        author_name = data['author']
        #author_user = User.objects.get(username = author_name)
        message = Message.objects.create(
                 author = author_name,
                 content = text_message)
        #self.our_chat.messages.add(message)
        content = {
              'command': 'new_message',
              'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)  
    
    def new_message_to_different_chats(self, data):
        #Сообщению необходимо добавить поле author_pk 
        text_message = data['content']
        chat_pk = data['chat_pk']
        author_pk = data['author_pk']
        chat = CustomUser.objects.get(pk = chat_pk).chat3
        message = Message.objects.create(
                 author = self.user.name,
                 content = text_message)
        chat.messages.add(message)
        content = {
              'command': 'new_message',
              'message': self.message_to_json(message, author_pk),
              'chat_pk': chat_pk,
              'author_pk': author_pk,
        }
        #print(str(content['chat_pk']))
        return self.send_chat_message(content)  

    def delete_message(self, data):
        primary_key = data['pk']
        msg = Message.objects.get(pk = primary_key)
        msg.delete()
        content = {
              'command': 'delete_message',
              'pk': primary_key,
        }
        return self.delete_chat_message(content)
    
    def edit_message(self, data):
        primary_key = data['pk']
        msg = Message.objects.get(pk = primary_key)
        if(msg.content != data['message']):
            msg.content = data['message']
            msg.save()
            return self.edit_chat_message(data)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        if(command == 'pre_load'):
            self.preLoadChats(text_data_json['author_pk'])
        if(command == 'new_message'):
            self.new_message_to_different_chats(text_data_json)
        if(command == 'delete_message'):
            self.delete_message(text_data_json)
        if(command == 'edit_message'):
            self.edit_message(text_data_json)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    
    # Send message to room group
    def send_chat_message(self, content):
            room_group_name = "chat" + str(content['chat_pk'])
            async_to_sync(self.channel_layer.group_send)(
            room_group_name,
            {
                'type': 'chat_message',
                'message': content
            })
    
    
    def send_message(self, content):
        text_data = json.dumps(content)
        self.send(text_data)

    def disconnect(self, close_code):
        if self.user.is_renter == True:
            for landlord in self.user.clients.all():
                chat = landlord.chat3
                room_group_name = "chat" + str(chat.pk)
                async_to_sync(self.channel_layer.group_add)(
                    room_group_name,
                    self.channel_name
                )
    #raise StopConsumer()
    

    # commands = {
    #     'pre_load' : pre_load_messages,
    #     'new_message' : new_message,
    #     'delete_message' : delete_message
    # }

    # # Send edited message to room group
    # def edit_chat_message(self, content):
    #         async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'edit_local_message',
    #             'message': content
    #         })
    
    # Delete message from room group
    def delete_chat_message(self, content):
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'delete_local_message',
                'content': content
            })
    
        # Receive 'edited message' from room group
    def edit_local_message(self, event):
        content = event['message']
        # 'Delete message' to WebSocket
        self.send(text_data=json.dumps(content))
    
        # Receive 'deleting message' from room group
    def delete_local_message(self, event):
        content = event['content']
        # 'Delete message' to WebSocket
        self.send(text_data=json.dumps(content))

#python3 manage.py runserver
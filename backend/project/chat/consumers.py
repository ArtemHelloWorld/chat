import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django_eventstream import send_event

import chat.models
import chat.serializers
import users.models


class ChatConsumer(WebsocketConsumer):
    def update_online_status(self, online_status):
        user = users.models.User.objects.get(pk=self.scope['user'].pk)
        user.is_online = online_status
        user.last_online = int(datetime.now().timestamp() * 1000)
        user.save()

        self.scope['user'] = user
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'online_status',
                'sender': self.scope['user'].id,
                'is_online': self.scope['user'].is_online,
                'last_online': self.scope['user'].last_online,
            }
        )

    def connect(self):
        print('connected')

        self.chat_pk = self.scope['chat_pk']
        self.chat_ = self.scope['chat_']
        self.chat_group_name = f'chat_{self.chat_pk}'

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name
        )
        self.accept()

        self.update_online_status(online_status=True)

    def disconnect(self, close_code):
        print('disconnected')

        self.update_online_status(online_status=False)

        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        print('receive')
        data_json = json.loads(text_data)

        if 'message' in data_json:
            message = data_json.get('message')
            print(f'message: {message}')

            message_bd = chat.models.Message.objects.create(
                chat=self.chat_,
                sender=self.scope['user'],
                text=message
            )
            data = {
                'type': 'chat_message',
                'pk': message_bd.pk,
                'text': message_bd.text,
                'sender': message_bd.sender.id,
                'sending_timestamp': message_bd.sending_timestamp
            }
            self.chat_.last_message = message_bd
            self.chat_.save()
            chat_data = {
                'id': self.chat_.id,
                'last_message_info': chat.serializers.MessageSerializer(message_bd).data,
            }
            send_event(f'notifications-{self.chat_.user1.id}', 'message', chat_data)
            send_event(f'notifications-{self.chat_.user2.id}', 'message', chat_data)
            async_to_sync(self.channel_layer.group_send)(self.chat_group_name, data)

        elif 'typing' in data_json:
            typing = data_json.get('typing')
            print(f'Typing: {typing}')

            if typing:
                self.chat_.status[self.scope['user'].id] = 'Печатает...'
            else:
                del self.chat_.status[self.scope['user'].id]

            self.chat_.save()
            chat_data = {
                'id': self.chat_.id,
                'status': self.chat_.status,
            }
            send_event(f'notifications-{self.chat_.user1.id}', 'message', chat_data)
            send_event(f'notifications-{self.chat_.user2.id}', 'message', chat_data)

            async_to_sync(self.channel_layer.group_send)(
                self.chat_group_name,
                {
                    'type': 'user_typing',
                    'typing': typing,
                    'sender': self.scope['user'].id
                }
            )
        elif 'mark_message_as_read' in data_json:
            message_pk = data_json.get('mark_message_as_read')
            print(f'Mark_message_as_read: {message_pk}')

            message = chat.models.Message.objects.get(pk=message_pk)
            message.is_read = True
            message.save()
            print('marked')

            async_to_sync(self.channel_layer.group_send)(
                self.chat_group_name,
                {
                    'type': 'mark_message_as_read',
                    'message_pk': message_pk
                }
            )

    def online_status(self, event):
        data = {
            'type': 'online_status',
            'sender': event.get('sender'),
            'is_online': event.get('is_online'),
            'last_online': event.get('last_online'),
        }
        self.send(text_data=json.dumps(data))

    def chat_message(self, event):
        # Отправка события 'новое сообщение'
        data = {
            'type': 'chat',
            'id': event.get('pk'),
            'text': event.get('text'),
            'sender': event.get('sender'),
            'sending_timestamp': event.get('sending_timestamp'),
        }

        self.send(text_data=json.dumps(data))

    def user_typing(self, event):
        # Отправка события о том, что пользователь начал или закончил печатать
        self.send(
            text_data=json.dumps(
                {
                    'type': 'user_typing',
                    'typing': event.get('typing'),
                    'sender': event.get('sender'),
                }
            )
        )

    def mark_message_as_read(self, event):
        # Отправка события о том, что пользователь прочитал сообщение
        self.send(
            text_data=json.dumps(
                {
                    'type': 'mark_message_as_read',
                    'message_pk': event.get('message_pk')
                }
            )
        )

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

import chat.models


class ChatConsumer(WebsocketConsumer):
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
        # async_to_sync(self.channel_layer.group_send)(
        #     self.chat_group_name,
        #     {
        #         'type': 'heart_beating',
        #         'heartbeat': True,
        #         'sender': self.scope['user'].username
        #     }
        # )
        self.scope['user'].last_online = timezone.now()
        self.scope['user'].save()

    def disconnect(self, close_code):
        print('disconnected')

        # async_to_sync(self.channel_layer.group_send)(
        #     self.chat_group_name,
        #     {
        #         'type': 'heart_beating',
        #         'heartbeat': False,
        #         'sender': self.scope['user'].username
        #     }
        # )

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

            async_to_sync(self.channel_layer.group_send)(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'pk': message_bd.pk,
                    'text': message,
                    'sender': self.scope['user'].id
                }
            )

        # elif 'heartbeat' in data_json:
        #     heartbeat = data_json.get('heartbeat')
        #     print(f'heartbeat {self.scope["user"].username} {heartbeat}')
        #
        #     if heartbeat:
        #         self.scope['user'].last_online = timezone.now()
        #         self.scope['user'].save()
        #
        #     async_to_sync(self.channel_layer.group_send)(
        #         self.chat_group_name,
        #         {
        #             'type': 'heart_beating',
        #             'heartbeat': heartbeat,
        #             'sender': self.scope['user'].username
        #         }
        #     )
        elif 'typing' in data_json:
            typing = data_json.get('typing')
            print(f'Typing: {typing}')

            async_to_sync(self.channel_layer.group_send)(
                self.chat_group_name,
                {
                    'type': 'user_typing',
                    'typing': typing,
                    'sender': self.scope['user'].username
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

    def chat_message(self, event):
        # Отправка события 'новое сообщение'
        timezone_now = timezone.now()
        current_date = timezone_now.strftime('%d.%m.%y')
        current_time = timezone_now.strftime('%H:%M')

        self.send(
            text_data=json.dumps(
                {
                    'type': 'chat',
                    'id': event.get('pk'),
                    'text': event.get('text'),
                    'sender': event.get('sender'),
                    'current_date': current_date,
                    'time_sending': current_time,
                }
            )
        )

    # def heart_beating(self, event):
    #     # Отправка события о том, что пользователь онлайн
    #     self.send(
    #         text_data=json.dumps(
    #             {
    #                 'type': 'heart_beating',
    #                 'heartbeat': event.get('heartbeat'),
    #                 'sender': event.get('sender')
    #             }
    #         )
    #     )

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

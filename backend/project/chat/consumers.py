import json

import asgiref.sync
import channels.generic.websocket
import channels.layers
import django_eventstream

import chat.models
import chat.serializers


class ReceiversMixin:
    """
    Методы обработки нового события от пользователя
    и отправки этого события всем пользователям группы
    """

    chat_: chat.models.Chat
    scope: dict
    channel_layer: channels.layers.InMemoryChannelLayer
    chat_group_name: str

    def message_receiver(self, data_json):
        message = data_json.get('message')
        file_id = data_json.get('file_id')
        print(f'message: {message}')

        message_bd = chat.models.Message.objects.create(
            chat=self.chat_,
            sender=self.scope['user'],
            text=message,
        )
        if file_id:
            message_bd.file = chat.models.MessageFile.objects.get(id=file_id)
            message_bd.save()

        data = {
            'type': 'chat_message',
            'pk': message_bd.pk,
            'text': message_bd.text,
            'file': message_bd.file.image.url if message_bd.file else None,
            'sender': message_bd.sender.id,
            'sending_timestamp': message_bd.sending_timestamp,
        }
        self.chat_.last_message = message_bd
        self.chat_.save()

        chat_data = {
            'id': self.chat_.id,
            'last_message_info': chat.serializers.MessageSerializer(
                message_bd
            ).data,
        }
        for user in self.chat_.users.all():
            django_eventstream.send_event(
                f'notifications-{user.id}', 'message', chat_data
            )
        asgiref.sync.async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name, data
        )

    def typing_receiver(self, data_json):
        typing = data_json.get('typing')
        print(f'Typing: {typing}')

        if typing:
            self.chat_.status[self.scope['user'].id] = 'Печатает...'
        else:
            self.chat_.status.pop(self.scope['user'].id)
        self.chat_.save()

        chat_data = {
            'id': self.chat_.id,
            'status': self.chat_.status,
        }
        # todo: а нужно ли отправлять всем
        for user in self.chat_.users.all():
            django_eventstream.send_event(
                f'notifications-{user.id}', 'message', chat_data
            )

        asgiref.sync.async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'user_typing',
                'sender': self.scope['user'].id,
                'typing': typing,
            },
        )

    def mark_message_as_read_receiver(self, data_json):
        message_pk = data_json.get('mark_message_as_read')
        print(f'Mark_message_as_read: {message_pk}')

        message = chat.models.Message.objects.get(pk=message_pk)
        message.is_read = True
        message.save()
        if self.chat_.last_message == message:
            chat_data = {
                'id': self.chat_.id,
                'last_message_info': chat.serializers.MessageSerializer(
                    message
                ).data,
            }
            for user in self.chat_.users.all():
                django_eventstream.send_event(
                    f'notifications-{user.id}', 'message', chat_data
                )

        asgiref.sync.async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {'type': 'mark_message_as_read', 'message_pk': message_pk},
        )


class HandlersMixin:
    """
    Методы обработки событий, созданных групповой рассылкой
    """

    def send(self, text_data=None, bytes_data=None, close=False):
        ...

    def _group_send_i_am_here(self, os_online: bool):
        ...

    def i_am_here(self, event):
        data = {
            'type': 'i_am_here',
            'sender': event.get('sender'),
            'is_online': event.get('is_online'),
        }
        self.send(text_data=json.dumps(data))

    def who_is_here(self, event):
        self._group_send_i_am_here(True)

    def chat_message(self, event):
        data = {
            'type': 'chat_message',
            'id': event.get('pk'),
            'text': event.get('text'),
            'file': event.get('file'),
            'sender': event.get('sender'),
            'sending_timestamp': event.get('sending_timestamp'),
        }

        self.send(text_data=json.dumps(data))

    def user_typing(self, event):
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
        self.send(
            text_data=json.dumps(
                {
                    'type': 'mark_message_as_read',
                    'message_pk': event.get('message_pk'),
                }
            )
        )


class ChatConsumer(
    ReceiversMixin, HandlersMixin, channels.generic.websocket.WebsocketConsumer
):
    def connect(self):
        print('connected')

        self.chat_pk = self.scope['chat_pk']
        self.chat_ = self.scope['chat_']
        self.chat_group_name = f'chat_{self.chat_pk}'

        asgiref.sync.async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name, self.channel_name
        )
        self.accept()

        self._group_send_i_am_here(True)
        self._grop_send_who_is_here()

    def disconnect(self, close_code):
        print('disconnected')
        self._group_send_i_am_here(os_online=False)

        asgiref.sync.async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        print('receive')
        data_json = json.loads(text_data)

        if 'message' in data_json:
            self.message_receiver(data_json)

        elif 'typing' in data_json:
            self.typing_receiver(data_json)

        elif 'mark_message_as_read' in data_json:
            self.mark_message_as_read_receiver(data_json)

    def _group_send_i_am_here(self, os_online: bool):
        asgiref.sync.async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'i_am_here',
                'sender': self.scope['user'].id,
                'is_online': os_online,
            },
        )

    def _grop_send_who_is_here(self):
        asgiref.sync.async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'who_is_here',
                'sender': self.scope['user'].id,
            },
        )

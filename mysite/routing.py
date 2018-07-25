
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.conf.urls import url

from chat.consumers import ChatConsumer
from post.consumers import PostConsumer


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
            url(r'^ws/$', PostConsumer),
        ])
    ),
})

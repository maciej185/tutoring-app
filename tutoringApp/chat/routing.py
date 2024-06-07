from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<tutor_id>\d+)/(?P<student_id>\d+)/$", consumers.NewChatConsumer.as_asgi())
]

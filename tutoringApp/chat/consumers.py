# chat/consumers.py
import json
from typing import Any

from channels.generic.websocket import AsyncWebsocketConsumer


class NewChatConsumer(AsyncWebsocketConsumer):
    """COnsumer for handling incoming requests sent via WebSockets"""

    async def connect(self) -> None:
        """Invoked once when the client connects to the Consumer."""
        self.tutor_id = self.scope["url_route"]["kwargs"]["tutor_id"]
        self.student_id = self.scope["url_route"]["kwargs"]["student_id"]

        self.group_name = f"chat_{self.tutor_id}_to_{self.student_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, _close_code) -> None:
        """Invoked when the connection is closed."""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data: str) -> None:
        """Handle receiving requests.

        The method parses the request's body and invokes appropriate methods
        for forwarding the message to everyone in the group.

        Args:
            text_data: A string containing the request's payload.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user_id"]

        await self.channel_layer.group_send(
            self.group_name, {"type": "chat_message", "message": message, "user_id": user_id}
        )

    async def chat_message(self, event: dict[str, Any]) -> None:
        """Send a request to everyone in the group.

        The method accepts a dictionary with values to be sent
        to everyone in the group, parses it to a string format
        and send the request out.
        """
        message = event["message"]
        user_id = event["user_id"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user_id": user_id}))

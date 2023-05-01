import json
from typing import Callable
import websockets

from homeassistant.core import HomeAssistant


class MSTeamsHub:
    """Hub for connecting to the MS teams websocket."""

    def __init__(
        self, hass: HomeAssistant, name: str, host: str, port: int, token: str
    ) -> None:
        self._host = host
        self._hass = hass
        self._name = name
        self._uri = f"ws://{host}:{port}?token={token}&protocol-version=1.0.0&manufacturer=MuteDeck&device=MuteDeck&app=MuteDeck&app-version=1.4"
        self._id = host.lower()
        self._callbacks = set()
        self._latest_message = None
        self._is_active = False

    async def test_endpoint(self) -> bool:
        """Test if we can subscribe to the websocket."""
        success = False
        async with websockets.connect(self._uri) as websocket:
            success = not websocket.closed

        return success

    async def update(self) -> None:
        async for websocket in websockets.connect(self._uri):
            try:
                self._is_active = not websocket.closed
                async for message in websocket:
                    self._latest_message = json.loads(message)
                    await self.publish_updates()
            except bwebsockets.WebSocketException:
                self._is_active = False
                continue
            self._is_active = not websocket.closed
            await self.publish_updates()

    @property
    def is_in_meeting(self):
        """Extract meeting status from latest message."""
        try:
            return self._latest_message["meetingUpdate"]["meetingState"]["isInMeeting"]
        except TypeError:
            return None

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback called when the state changes."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        for callback in self._callbacks:
            callback()

    @property
    def available(self) -> bool:
        """Available if the websockets connection has value and is not closed."""
        return self._is_active

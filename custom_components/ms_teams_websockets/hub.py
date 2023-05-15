"""Contains the MSTeamsHub class."""

import json
import websockets

from collections.abc import Callable
from datetime import datetime

from homeassistant.core import HomeAssistant

from . import const


class MSTeamsHub:
    """Hub for connecting to the MS teams websocket."""

    def __init__(
        self, hass: HomeAssistant, name: str, host: str, port: int, token: str
    ) -> None:
        """Initialise the class."""
        self._host = host
        self._hass = hass
        self._name = name
        self._uri = f"ws://{host}:{port}?token={token}&protocol-version=1.0.0&manufacturer=MuteDeck&device=MuteDeck&app=MuteDeck&app-version=1.4"
        self._id = host.lower()
        self._callbacks = set()
        self._is_active = False
        self._is_in_meeting = False
        self._is_muted = False
        self._is_camera_on = False
        self._is_hand_raised = False
        self._is_recording_on = False
        self._is_background_blurred = False

    async def test_endpoint(self) -> bool:
        """Test if we can subscribe to the websocket."""
        success = False
        async with websockets.connect(self._uri) as websocket:
            success = not websocket.closed

        return success

    async def update(self) -> None:
        """Background task to loop websocket updates."""
        async for websocket in websockets.connect(self._uri):
            try:
                self._is_active = not websocket.closed
                async for message in websocket:
                    latest_message = json.loads(message)
                    meeting_state = latest_message["meetingUpdate"]["meetingState"]
                    self._is_in_meeting = meeting_state["isInMeeting"]
                    self._is_muted = meeting_state["isMuted"]
                    self._is_camera_on = meeting_state["isCameraOn"]
                    self._is_hand_raised = meeting_state["isHandRaised"]
                    self._is_recording_on = meeting_state["isRecordingOn"]
                    self._is_background_blurred = meeting_state["isBackgroundBlurred"]
                    await self.publish_updates()
            except websockets.WebSocketException:
                self._is_active = False
                continue
            self._is_active = not websocket.closed
            await self.publish_updates()

    @property
    def is_in_meeting(self) -> bool:
        """Return meeting status from latest message."""
        return self._is_in_meeting

    @property
    def is_muted(self) -> bool:
        """Return muted status from latest message."""
        return self._is_muted

    @property
    def is_camera_on(self) -> bool:
        """Return camera status from latest message."""
        return self._is_camera_on

    @property
    def is_hand_raised(self) -> bool:
        """Return hand raised status from latest message."""
        return self._is_hand_raised

    @property
    def is_recording_on(self) -> bool:
        """Return recording status from latest message."""
        return self._is_recording_on

    @property
    def is_background_blurred(self) -> bool:
        """Return background blur status from latest message."""
        return self._is_background_blurred

    async def perform_action(self, message) -> None:
        """Send a constructed message to the websockets endpoint."""
        message.update(const.ACTION_BASE_MESSAGE)
        message["timestamp"] = datetime.now().timestamp()
        async with websockets.connect(self._uri) as websocket:
            await websocket.send(json.dumps(message))

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback called when the state changes."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        """Call all callbacks on update."""
        for callback in self._callbacks:
            callback()

    @property
    def available(self) -> bool:
        """Available if the websockets connection has value and is not closed."""
        return self._is_active

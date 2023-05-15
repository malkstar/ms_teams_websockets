"""Constants for the MS Teams Websockets integration."""

DOMAIN: str = "ms_teams_websockets"

ACTION_GET_UPDATE: dict = {
    "service": "query-meeting-state",
    "action": "query-meeting-state",
}
ACTION_TOGGLE_MUTE: dict = {"service": "toggle-mute", "action": "toggle-mute"}
ACTION_TOGGLE_VIDEO: dict = {"service": "toggle-video", "action": "toggle-video"}
ACTION_LEAVE_MEETING: dict = {"service": "call", "action": "leave-call"}
ACTION_BLUR_BACKGROUND: dict = {
    "service": "background-blur",
    "action": "toggle-background-blur",
}
ACTION_RAISE_HAND: dict = {"service": "raise-hand", "action": "toggle-hand"}
ACTION_REACT_APPLAUSE: dict = {"service": "call", "action": "react-applause"}
ACTION_REACT_LAUGH: dict = {"service": "call", "action": "react-laugh"}
ACTION_REACT_LIKE: dict = {"service": "call", "action": "react-like"}
ACTION_REACT_LOVE: dict = {"service": "call", "action": "react-love"}
ACTION_BASE_MESSAGE: dict = {
    "apiVersion": "1.0.0",
    "manufacturer": "Elgato",
    "device": "StreamDeck",
}

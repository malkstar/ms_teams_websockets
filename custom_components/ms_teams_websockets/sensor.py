"""Contains the Entity classes."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .const import DOMAIN
from .entity import MSTeamsBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for setup hub object."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            InMeetingEntity(hub),
            MutedEntity(hub),
            CameraOnEntity(hub),
            HandRaisedEntity(hub),
            RecordingOnEntity(hub),
            BackgroundBlurredEntity(hub),
        ]
    )


class InMeetingEntity(MSTeamsBaseEntity):
    """In meeting entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_is_in_meeting"
        self._attr_name = f"{hub._name} is in meeting"

    @property
    def state(self) -> bool:
        """Return the state of the sensor."""

        return self._hub.is_in_meeting


class MutedEntity(MSTeamsBaseEntity):
    """Muted entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_is_muted"
        self._attr_name = f"{hub._name} is muted"

    @property
    def state(self) -> bool:
        """Return the state of the sensor."""

        return self._hub.is_muted


class CameraOnEntity(MSTeamsBaseEntity):
    """Camera on entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_has_camera_on"
        self._attr_name = f"{hub._name} has camera on"

    @property
    def state(self) -> bool:
        """Return the state of the sensor."""

        return self._hub.is_camera_on


class HandRaisedEntity(MSTeamsBaseEntity):
    """Hand raised entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_has_hand_raised"
        self._attr_name = f"{hub._name} has hand raised"

    @property
    def state(self) -> bool:
        """Return the state of the sensor."""

        return self._hub.is_hand_raised


class RecordingOnEntity(MSTeamsBaseEntity):
    """Recording on entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_has_recording_on"
        self._attr_name = f"{hub._name} has recording on"

    @property
    def state(self) -> bool:
        """Return the state of the sensor."""

        return self._hub.is_recording_on


class BackgroundBlurredEntity(MSTeamsBaseEntity):
    """Background blurred entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_has_background_blurred"
        self._attr_name = f"{hub._name} has background blurred"

    @property
    def state(self) -> bool:
        """Return the state of the sensor."""

        return self._hub.is_background_blurred

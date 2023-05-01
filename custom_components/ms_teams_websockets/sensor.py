"""Contains the Entity classes."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity

from .const import DOMAIN


async def async_setup_entry(hass, config_entry: ConfigEntry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([InMeetingEntity(hub)])


class SensorBase(Entity):
    """Base clase for the MS teams sensors."""

    should_poll = False

    def __init__(self, hub):
        """Initialize the sensor."""
        self._hub = hub

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._hub._id)},
            "name": f"Teams {self._hub._name}",
        }

    @property
    def available(self) -> bool:
        """Return True if websocket is available."""
        return self._hub.available

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._hub.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._hub.remove_callback(self.async_write_ha_state)


class InMeetingEntity(SensorBase):
    """In meeting entity."""

    should_poll = False

    def __init__(self, hub):
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_is_in_meeting"
        self._attr_name = f"{hub._name} is in meeting"

    @property
    def state(self):
        """Return the state of the sensor."""

        return self._hub.is_in_meeting

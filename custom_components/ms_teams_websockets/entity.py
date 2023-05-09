"""Contains the base entity for the integration."""

from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import DOMAIN
from .hub import MSTeamsHub


class MSTeamsBaseEntity(Entity):
    """Base entity for shared functionalities."""

    _attr_should_poll: str = False

    def __init__(self, hub) -> None:
        """Initialize the entity with the hub."""
        self._hub: MSTeamsHub = hub

    @property
    def device_info(self) -> DeviceInfo:
        """Return information to link this entity with the correct device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._hub._id)},
            model=f"{self._hub._name} client at {self._hub._host}",
            name=f"{self._hub._name} Teams",
            manufacturer="Microsoft Teams",
        )

    @property
    def available(self) -> bool:
        """Return True if websocket is available."""
        return self._hub.available

    async def async_added_to_hass(self) -> None:
        """Run when this Entity has been added to HA."""
        self._hub.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self) -> None:
        """Entity being removed from hass."""
        self._hub.remove_callback(self.async_write_ha_state)

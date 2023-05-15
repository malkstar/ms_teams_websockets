"""The MS Teams Presence integration."""
from __future__ import annotations


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    Platform,
    CONF_PORT,
    CONF_HOST,
    CONF_FRIENDLY_NAME,
    CONF_API_TOKEN,
)

from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .hub import MSTeamsHub


PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MS Teams Presence from a config entry."""

    hub = MSTeamsHub(
        hass,
        entry.data[CONF_FRIENDLY_NAME],
        entry.data[CONF_HOST],
        entry.data[CONF_PORT],
        entry.data[CONF_API_TOKEN],
    )

    entry.async_create_background_task(hass, hub.update(), "ms_teams_update")
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

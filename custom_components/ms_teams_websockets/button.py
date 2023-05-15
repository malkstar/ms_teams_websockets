"""Buttons to perform Teams actions."""

from dataclasses import dataclass

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from . import const
from .entity import MSTeamsBaseEntity
from .hub import MSTeamsHub


@dataclass
class MSTeamsButtonDescriptionMixin:
    """Mixin to add action_data to ButtonEntityDescription class."""

    action_data: dict


@dataclass
class MSTeamsButtonDescription(ButtonEntityDescription, MSTeamsButtonDescriptionMixin):
    """Class for adding Mixin class to base ButtonEntityDescription."""


BUTTONS: tuple[MSTeamsButtonDescription] = (
    MSTeamsButtonDescription(
        name="Get meeting update",
        key="get_update",
        translation_key="get_update",
        device_class=ButtonDeviceClass.UPDATE,
        action_data=const.ACTION_GET_UPDATE,
    ),
    MSTeamsButtonDescription(
        name="Toggle mute",
        key="toggle_mute",
        translation_key="toggle_mute",
        action_data=const.ACTION_TOGGLE_MUTE,
    ),
    MSTeamsButtonDescription(
        name="Toggle video",
        key="toggle_video",
        translation_key="toggle_video",
        action_data=const.ACTION_TOGGLE_VIDEO,
    ),
    MSTeamsButtonDescription(
        name="Leave meeting",
        key="leave_meeting",
        translation_key="leave_meeting",
        action_data=const.ACTION_LEAVE_MEETING,
    ),
    MSTeamsButtonDescription(
        name="Blur background",
        key="blur_background",
        translation_key="blur_background",
        action_data=const.ACTION_BLUR_BACKGROUND,
    ),
    MSTeamsButtonDescription(
        name="Raise hand",
        key="raise_hand",
        translation_key="raise_hand",
        action_data=const.ACTION_RAISE_HAND,
    ),
    MSTeamsButtonDescription(
        name="React applause",
        key="react_applause",
        translation_key="react_applause",
        action_data=const.ACTION_REACT_APPLAUSE,
    ),
    MSTeamsButtonDescription(
        name="React laugh",
        key="react_laugh",
        translation_key="react_laugh",
        action_data=const.ACTION_REACT_LAUGH,
    ),
    MSTeamsButtonDescription(
        name="React like",
        key="react_like",
        translation_key="react_like",
        action_data=const.ACTION_REACT_LIKE,
    ),
    MSTeamsButtonDescription(
        name="React love",
        key="react_love",
        translation_key="react_love",
        action_data=const.ACTION_REACT_LOVE,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add buttons for setup hub object."""

    hub = hass.data[const.DOMAIN][config_entry.entry_id]

    async_add_entities(TeamsButton(hub, description) for description in BUTTONS)


class TeamsButton(MSTeamsBaseEntity, ButtonEntity):
    """Button class which will run the hub.perform_action method with configured description action_data."""

    def __init__(
        self,
        hub: MSTeamsHub,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_{description.key}"
        self.entity_description = description

    async def async_press(self) -> None:
        """Trigger the button action."""
        await self._hub.perform_action(self.entity_description.action_data)

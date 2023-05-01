[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)


# Teams Websockets integration

This integration exposes your Teams client's local websockets API data in Home Assistant sensors.


## Installation

Either:

A) Add the custom repository in HACS, install it, then use the usual add integration functionality.

B) Copy the ``custom_components/ms_teams_websockets`` into your HA ``custom_components`` folder.


## Setup

Follow [this guide](https://support.microsoft.com/en-us/office/connect-third-party-devices-to-teams-aabca9f2-47bb-407f-9f9b-81a104a883d6) to enable the API on the client machine. Use this token when setting up the integration.


## How?

[Teams v1.6+ has a websocket API that can be used for third parties to connect to Teams and get information about and manage calls. It’s first used in the Stream Deck Plugin.](https://techcommunity.microsoft.com/t5/microsoft-teams-blog/delivering-new-webinar-experiences-with-microsoft-teams/ba-p/3725145)


## Credits

I used the information from [this page](https://lostdomain.notion.site/Microsoft-Teams-WebSocket-API-5c042838bc3e4731bdfe679e864ab52a). Unfortunately I am unsure of the author to give proper credit.


## Roadmap

I plan to implement all the data returned as sensors, and eventually make the actions available too.
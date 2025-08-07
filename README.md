# allunited_homeassistant
An integration for adding AllUnited reservations into Home Assistant

## Installation
Copy the `allunited` folder to the `custom_components` folder and restart Home Assistant

## Configuration
When adding the integration, choose a name and enter the URL where the required planningboard is located.
A Calendar entity will be added that contains all reservations for today, on all courts.

### Sub entries
The AllUnited integration supports Sub-entries.
You can configure groups of courts, new Calendar entities will be created that only contain reservations for these courts.

## TODO:
- Add sensors that show the last successful update date, this can be used to notify administrators of failures.
"""Platform for sensor integration."""
from hashlib import new
from cv2 import add, line
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import (
    DEVICE_CLASS_MONETARY,
    SensorEntity,
    SensorEntityDescription,
)

""" External Imports """
import requests
import json
import datetime
import logging


""" Constants """
NATIVE_UNIT_OF_MEASUREMENT = "Kč/kWh"
DEVICE_CLASS = "monetary"
COURSE_CODE = "EUR"

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([CZCurrencyRates()], update_before_add=True)

class CZCurrencyRates(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._value = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'CZ Currency Rates'

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self._value

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return DEVICE_CLASS

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def extra_state_attributes(self):
        """Return other attributes of the sensor."""
        return self._attr


    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self.get_course()

    def get_course(self):

        try:
          
            response = requests.get(url="https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt").text

            tst = response.split("\n")

            del tst[0]
            del tst[0]
            del tst[len(tst) -1]

            for item in tst:
                lineData = item.split("|")

                attr = []

                attr.append(float(lineData[4].replace(",", ".")) / lineData[2])

                if lineData[3] == COURSE_CODE:
                    
                    course = float(lineData[4].replace(",", "."))

            self._value = course
            self._attr = attr
            self._available = True
        except:
          self._available = False
          _LOGGER.exception("Error occured while retrieving data from cnb.cz.")

        

        

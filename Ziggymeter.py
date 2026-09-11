"""ZHA quirks for ZiggyMeter ZG-400.

SPDX-License-Identifier: CC0

Temperature fix
---------------
The ZG-400 reports device temperature via the Device Temperature Configuration
cluster (0x0002, attribute CurrentTemperature 0x0000) in whole degrees Celsius
(units = 1 °C, as required by the ZCL spec for that cluster).

ZHA/zigpy maps this attribute with a multiplier of 0.01 (same as the Temperature
Measurement cluster 0x0402), which causes the displayed value to be 100× too
small (e.g. 30 °C appears as 0.3 °C).

The quirk below replaces the cluster parser with one that reports MULTIPLIER=100
and DIVISOR=1 so that the raw integer value is passed through unchanged in °C.

Switch Rename
-------------
Two switches are renamed for better clarity.


Installation
------------
Place this file in your ZHA custom_quirks directory, e.g.:

    /config/custom_quirks/Ziggymeter.py

Then add/confirm in configuration.yaml:

    zha:
      custom_quirks_path: /config/custom_quirks
"""

from zigpy.quirks.v2 import CustomDeviceV2, QuirkBuilder
from zigpy.zcl.clusters.general import DeviceTemperature as ZigpyDeviceTemperature, OnOff


class ZG400(CustomDeviceV2):
    """ZiggyMeter ZG-400 quirk."""


class ZiggyMeterDeviceTempCluster(ZigpyDeviceTemperature):
    def _update_attribute(self, attrid, value):
        if attrid == self.AttributeDefs.current_temperature.id and isinstance(value, (int, float)):
            value = value * 100
        super()._update_attribute(attrid, value)


(
    QuirkBuilder("ZiggyMeter", "ZG-400")
    .device_class(ZG400)
    .replaces(ZiggyMeterDeviceTempCluster, endpoint_id=1)
    .change_entity_metadata(endpoint_id=1, cluster_id=OnOff.cluster_id, new_translation_key="ziggymeter_wifi", new_fallback_name="Activate WiFi")
    .change_entity_metadata(endpoint_id=2, cluster_id=OnOff.cluster_id, new_translation_key="ziggymeter_readout", new_fallback_name="Readout Trigger")
    .add_to_registry()
)

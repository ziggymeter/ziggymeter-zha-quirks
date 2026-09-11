# ZiggyMeter ZHA Quirks

Custom ZHA quirk for the [ZiggyMeter ZG-400](https://ziggymeter.com).

## What it does

- Fixes the device temperature value reported by the ZG-400.
- Renames the device switches for clearer controls:
  - **Activate WiFi** (endpoint 1)
  - **Readout Trigger** (endpoint 2)

### Temperature correction

The ZG-400 reports its device temperature through the Device Temperature Configuration cluster (`0x0002`), in whole degrees Celsius. ZHA/zigpy normally applies a `0.01` multiplier intended for the Temperature Measurement cluster, making a value such as `30 °C` appear as `0.3 °C`.

This quirk adjusts the value so the reported temperature is displayed correctly in degrees Celsius.

## Installation

1. Copy [`Ziggymeter.py`](Ziggymeter.py) to your Home Assistant ZHA custom quirks directory, for example:

   ```text
   /config/custom_quirks/Ziggymeter.py
   ```

2. Add or confirm the custom quirks path in `configuration.yaml`:

   ```yaml
   zha:
     custom_quirks_path: /config/custom_quirks
   ```

3. Restart Home Assistant and re-pair or reload the ZiggyMeter device if needed.

## Supported device

- Manufacturer: `ZiggyMeter`
- Model: `ZG-400`

## License

This project is released under [CC0](LICENSE).

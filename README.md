# MQTT Duration Trigger

MQTT Duration Trigger is a custom component for Home Assistant that allows you to trigger actions based on the duration of MQTT messages. It classifies button presses as "short" or "long" depending on a configurable threshold.

## Features

- Configure multiple input and output MQTT topics
- Customizable duration threshold for distinguishing between short and long presses
- Integrates seamlessly with Home Assistant's MQTT component

## Installation

### HACS (Recommended)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Search for "MQTT Duration Trigger" in HACS and install it.
3. Restart Home Assistant.

### Manual Installation

1. Copy the `mqtt_duration_trigger` folder into your `custom_components` directory in your Home Assistant configuration directory.
2. Restart Home Assistant.

## Configuration

Add the following to your `configuration.yaml` file:

```yaml
mqtt_duration_trigger:
  threshold: 1.0
  topics:
    - input_topic: "nspanel/Living Room Panel/r1_state"
      output_topic: "nspanel/Living Room Panel/r1_trigger"
    - input_topic: "nspanel/Living Room Panel/r2_state"
      output_topic: "nspanel/Living Room Panel/r2_trigger"
```

### Configuration Variables

- **threshold** (*Optional*): The duration threshold in seconds to distinguish between short and long presses. Default is 1.0 second.
- **topics** (*Required*): A list of topic pairs.
  - **input_topic** (*Required*): The MQTT topic to subscribe to for button state changes.
  - **output_topic** (*Required*): The MQTT topic to publish the trigger message to.

## Usage

The component subscribes to the specified input topics. When it receives a message:

1. If the payload is "1", it marks the start of a button press.
2. If the payload is "0", it calculates the duration of the press.
3. It then publishes a message to the corresponding output topic:
   - If the duration is less than the threshold, it publishes "{button_name}_short"
   - If the duration is greater than or equal to the threshold, it publishes "{button_name}_long"

The {button_name} is extracted from the input topic, assuming it's in the format "prefix/device_name/button_name_state".

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

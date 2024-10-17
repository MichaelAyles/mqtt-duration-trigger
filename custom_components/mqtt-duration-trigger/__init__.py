import asyncio
import voluptuous as vol
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.components import mqtt

from .const import DOMAIN, CONF_TOPICS, CONF_THRESHOLD

TOPIC_SCHEMA = vol.Schema({
    vol.Required("input_topic"): cv.string,
    vol.Required("output_topic"): cv.string,
})

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({
            vol.Required(CONF_TOPICS): vol.All(cv.ensure_list, [TOPIC_SCHEMA]),
            vol.Optional(CONF_THRESHOLD, default=1.0): cv.positive_float,
        })
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the MQTT Duration Trigger component."""
    conf = config[DOMAIN]
    topics = conf[CONF_TOPICS]
    threshold = conf[CONF_THRESHOLD]

    topic_states = {}

    @callback
    async def message_received(msg):
        """Handle received MQTT messages."""
        topic = msg.topic
        payload = msg.payload
        current_time = asyncio.get_event_loop().time()

        if topic not in topic_states:
            return

        if payload == "1":  # On state
            topic_states[topic]["last_on"] = current_time
        elif payload == "0" and topic_states[topic]["last_on"] is not None:  # Off state
            duration = current_time - topic_states[topic]["last_on"]
            topic_states[topic]["last_on"] = None

            output_topic = topic_states[topic]["output_topic"]
            button_name = topic.split('/')[-1].split('_')[0]  # Extract 'r1' or 'r2' from the topic

            message = f"{button_name}_short" if duration < threshold else f"{button_name}_long"
            
            # Publish the message
            await mqtt.async_publish(hass, output_topic, message)

    for topic_config in topics:
        input_topic = topic_config["input_topic"]
        output_topic = topic_config["output_topic"]
        topic_states[input_topic] = {
            "last_on": None,
            "output_topic": output_topic
        }
        
        # Subscribe to the input topic
        await mqtt.async_subscribe(hass, input_topic, message_received)

    return True
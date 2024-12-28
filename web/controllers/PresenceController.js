import mqtt from 'mqtt';

class PresenceController {
    constructor() {
        this.presenceData = {}; // Object to store presence data
        this.initMQTT();
    }

    initMQTT() {
        // MQTT broker details
        const brokerUrl = "mqtt://broker.emqx.io:1883";
        const topic = "olark/home/presence";

        // Connect to the broker
        const client = mqtt.connect(brokerUrl);

        // Handle connection events
        client.on('connect', () => {
            console.log("Connected to MQTT broker");
            client.subscribe(topic, { qos: 1 }, (err) => {
                if (err) {
                    console.error(`Failed to subscribe to topic '${topic}':`, err);
                } else {
                    console.log(`Subscribed to topic '${topic}'`);
                }
            });
        });

        // Handle incoming messages
        client.on('message', (topic, message) => {
            try {
                const payload = JSON.parse(message.toString());
                console.log(`Received message: ${JSON.stringify(payload)}`);
                this.presenceData = payload; // Store the payload
            } catch (err) {
                console.error("Error parsing MQTT message:", err);
            }
        });

        // Handle errors
        client.on('error', (err) => {
            console.error("MQTT Error:", err);
        });
    }

    getPresenceData() {
        // Return the current presence data
        return Object.keys(this.presenceData).length > 0 ? this.presenceData : null;
    }
}

export default new PresenceController();

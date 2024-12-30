import mqtt from 'mqtt';

class PresenceController {
    constructor() {
        this.presenceData = {}; 
        this.initMQTT();
    }

    initMQTT() {
        const brokerUrl = "mqtt://broker.emqx.io:1883";
        const topic = "olark/home/presence";

        const client = mqtt.connect(brokerUrl);
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

        client.on('message', (topic, message) => {
            try {
                const payload = JSON.parse(message.toString());
                console.log(`Received message: ${JSON.stringify(payload)}`);
                this.presenceData = payload; 
            } catch (err) {
                console.error("Error parsing MQTT message:", err);
            }
        });

        client.on('error', (err) => {
            console.error("MQTT Error:", err);
        });
    }

    getPresenceData() {
        return Object.keys(this.presenceData).length > 0 ? this.presenceData : null;
    }
}

export default new PresenceController();

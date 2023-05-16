from confluent_kafka import Producer
import json

kafka_conf = {
    "bootstrap.servers" : "localhost:9092"
}

producer = Producer(kafka_conf)

razred = {
    "godina" : "2",
    "odjeljenje": "a"
}

razred_json = json.dumps(razred)

producer.produce("topic_razred", razred_json)

producer.flush()

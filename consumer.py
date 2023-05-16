from confluent_kafka import Consumer
import json
from model import *
from model.relacije import *

kafka_conf = {
    "bootstrap.servers" : "localhost:9092",
    "group.id" : "mojagrupa",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(kafka_conf)

consumer.subscribe(["topic_razred"])

while True:
    message = consumer.poll(1.0)
    if message:
        razred = json.loads(message.value().decode("utf8"))
        print(razred)
        db_razred = Razred(godina=razred["godina"], odjeljenje=razred["odjeljenje"])
        session.add(db_razred)
        session.commit()

consumer.close()

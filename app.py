from model import *
from model.relacije import *
from model.cache import region
from flask import Flask, request, render_template
from flask import jsonify
import json
from kafka import KafkaProducer, KafkaConsumer

app = Flask(__name__)

def json_serializer(data):
    return jsonify(data)

def json_deserializer():
    return request.get_json()

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=json_serializer
)

@app.route("/")
def index ():
    classes = session.query(Razred).all()
    consumer = KafkaConsumer(
        'razred',
        bootstrap_servers=['kafka:9092'],
        value_deserializer=json_deserializer,
        group_id='test-group',
        auto_offset_reset='earliest'
    )
    def consume_classes ():
       for message in consumer:
            razred = message.value
            yield razred

    return stream_template('classes.html', classes=classes, stream=consume_classes())

@app.route("/classes/delete/<int:id_razreda>", methods=["DELETE"])
def delete_class(id_razreda):
    # ID se sada prenosi putem URL-a
    # Dohvati objekt Razred sa navedenim ID-om
    razred = session.query(Razred).get(id_razreda)

    if razred:  # ako Razred s ovim ID-om postoji
        session.delete(razred)
        session.commit()
        # Uspješno izbrisano
        return jsonify({'message': f'Razred sa ID {id_razreda} je izbrisan.'}), 200
    else:
        # Nema Razreda s ovim ID-om
        return jsonify({'message': f'Nema razreda s ID {id_razreda}.'}), 404

@app.route("/classes/<int:id_razreda>", methods=["GET"])
def get_class(id_razreda):
    razred = region.get_or_create(
        f'Razred:{id_razreda}', 
        creator=lambda: session.query(Razred).get(id_razreda),
        expiration_time=60  # The time after which to expire the cache
    )
    if razred:
        # pretvoriti objekt Razred u rječnik
        # Uspješno dohvaćeno
        return jsonify(vars(razred)), 200
    else:
        # Nema Razreda s ovim ID-om
        return jsonify({'message': f'Nema razreda s ID {id_razreda}.'}), 404

@app.route("/classes/edit", methods=["PUT"])
def edit_class():
    id_razreda = request.form.get("ID_razreda")
    godina = request.form.get("godina")
    odjeljenje = request.form.get("odjeljenje")

    if id_razreda:  
        # Dohvati objekt Razred sa navedenim ID-om
        razred = session.query(Razred).get(id_razreda)
        if razred:  # ako Razred s ovim ID-om postoji
            # Ažurirati atribute objekta Razred
            if godina: 
                razred.godina = godina
            if odjeljenje: 
                razred.odjeljenje = odjeljenje
            session.commit()
            # Uspješno ažurirano
            return jsonify({'message': f'Razred sa ID {id_razreda} je ažuriran.'}), 200
        else:
            # Nema Razreda s ovim ID-om
            return jsonify({'message': f'Nema razreda s ID {id_razreda}.'}), 404
    else:
        # Nije pružen ID
        return jsonify({'message': 'ID nije pružen.'}), 400

@app.route("/classes/add", methods=["POST"])
def add_class():
    # Dohvati 'godina' i 'odjeljenje'
    godina = request.form.get("godina")
    odjeljenje = request.form.get("odjeljenje")

    # Dodaj novi razred
    razred = Razred(godina=godina, odjeljenje=odjeljenje)
    session.add(razred)
    session.commit()

    producer.send("razred", vars(razred))
    producer.flush()

    # Dobra je praksa vratiti ispravan JSON zahtjev
    return jsonify({'message': 'Dodan novi razred u bazu.'})


def stream_template(template_name, **context):
    """Enabling streaming back results to app"""
    app.update_template_context(context)
    template = app.jinja_env.get_template(template_name)
    streaming = template.stream(context)
    return streaming
from model import *
from model.relacije import *
from model.cache import region
from flask import Flask, request, render_template
from flask import jsonify
import json
from kafka import KafkaProducer, KafkaConsumer
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=json_serializer
)

consumer = KafkaConsumer(
    'razred',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=json_deserializer,
    group_id='test-group',
    auto_offset_reset='earliest'
)

kafka_thread = None


@app.route("/")
def index ():
    classes = session.query(Razred).all()
    return render_template('classes.html', classes=classes)

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
        return jsonify([{"ID_razreda": razred.ID_razreda, "godina": razred.godina, "odjeljenje": razred.odjeljenje}]), 200
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

            producer.send("razred", [{"ID_razreda": razred.ID_razreda, "godina": razred.godina, "odjeljenje": razred.odjeljenje}])
            producer.flush()

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

    producer.send("razred", [{"ID_razreda": razred.ID_razreda, "godina": razred.godina, "odjeljenje": razred.odjeljenje}])
    producer.flush()

    # Dobra je praksa vratiti ispravan JSON zahtjev
    return jsonify({'message': 'Dodan novi razred u bazu.'})

@socketio.on('connect', namespace='/kafka')
def connect():
    global kafka_thread
    if kafka_thread is None or not kafka_thread.is_alive():
        kafka_thread = threading.Thread(target=kafka_consumer)
        kafka_thread.start()

def kafka_consumer():
    for poruka in consumer:
        razred = poruka.value
        socketio.emit('data', {'razred': razred}, namespace='/kafka')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
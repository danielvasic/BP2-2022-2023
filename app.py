from model import *
from model.relacije import *
from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/")
def index ():
    classes = session.query(Razred).all()
    items = []
    for item in classes:
        items.append(
            {
                "id": item.ID_razreda, 
                "godina": item.godina, 
                "odjeljenje":item.odjeljenje
            }
        )
    return json.dumps(items)

@app.route("/classes/add")
def add_class ():
    godina = request.args.get("godina")
    odjeljenje = request.args.get("odjeljenje")
    razred = Razred(godina=godina, odjeljenje=odjeljenje)
    session.add(razred)
    session.commit()
    return "{'message': 'Dodan novi razred u bazu.'}"
